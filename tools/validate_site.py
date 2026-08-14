"""Valida referencias locales y reglas estructurales del sitio estático."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}
LEGACY_PREFIXES = ("css/", "img/", "js/", "lib/", "ser/")


class ReferenceParser(HTMLParser):
    """Recoge rutas y detecta atributos repetidos dentro de una etiqueta."""

    def __init__(self, source: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.source = source
        self.references: list[tuple[int, str, str]] = []
        self.errors: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        line, _ = self.getpos()
        names = [name for name, _ in attrs]
        duplicates = sorted({name for name in names if names.count(name) > 1})
        if duplicates:
            self.errors.append(
                f"{self.source.name}:{line}: atributos repetidos: {', '.join(duplicates)}"
            )

        for name, value in attrs:
            if name in {"href", "src"} and value:
                self.references.append((line, name, value.strip()))


def local_target(raw_reference: str) -> Path | None:
    """Convierte una referencia local en una ruta del proyecto."""

    if not raw_reference or raw_reference.startswith("#"):
        return None
    parsed = urlsplit(raw_reference)
    if parsed.scheme.lower() in IGNORED_SCHEMES or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if not path:
        return None
    return ROOT / path.lstrip("/")


def validate_html(path: Path) -> list[str]:
    """Valida sintaxis estructural simple y recursos enlazados por una página."""

    text = path.read_text(encoding="utf-8-sig")
    parser = ReferenceParser(path)
    parser.feed(text)
    errors = list(parser.errors)

    if re.search(r"<style(?:\s|>)", text, flags=re.IGNORECASE):
        errors.append(f"{path.name}: contiene CSS incrustado; muévelo a assets/css/pages/")

    for line, attribute, reference in parser.references:
        normalized = reference.replace("\\", "/")
        if normalized.startswith(LEGACY_PREFIXES):
            errors.append(f"{path.name}:{line}: ruta antigua en {attribute}=\"{reference}\"")
        target = local_target(reference)
        if target is not None and not target.exists():
            errors.append(f"{path.name}:{line}: no existe {reference}")

    return errors


def validate_css(path: Path) -> list[str]:
    """Comprueba los recursos locales declarados con url() en CSS."""

    errors: list[str] = []
    text = path.read_text(encoding="utf-8-sig")
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in re.finditer(r"url\(\s*(['\"]?)(.*?)\1\s*\)", line):
            reference = match.group(2).strip()
            parsed = urlsplit(reference)
            if not reference or parsed.scheme in IGNORED_SCHEMES or reference.startswith("#"):
                continue
            target = (path.parent / unquote(parsed.path)).resolve()
            if not target.exists():
                errors.append(f"{path.relative_to(ROOT)}:{line_number}: no existe {reference}")
    return errors


def main() -> int:
    """Ejecuta todas las comprobaciones y devuelve un código apto para automatización."""

    errors: list[str] = []
    html_files = sorted(ROOT.glob("*.html"))
    css_files = sorted((ROOT / "assets" / "css").rglob("*.css"))

    for html_file in html_files:
        errors.extend(validate_html(html_file))
    for css_file in css_files:
        errors.extend(validate_css(css_file))

    if errors:
        print("Se encontraron problemas:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validación correcta: {len(html_files)} páginas y {len(css_files)} hojas de estilo.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
