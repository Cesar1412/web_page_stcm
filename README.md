# Sitio web de STCM

Sitio corporativo estático y multipágina de STCM. El proyecto está organizado para que cada tipo de recurso tenga una responsabilidad clara y para que las páginas con diseño personalizado mantengan sus estilos aislados.

## Estructura principal

- `index.html` y `*.html`: páginas públicas. Se mantienen en la raíz para conservar las URL existentes.
- `assets/css/main.css`: estilos compartidos por todo el sitio.
- `assets/css/pages/`: estilos exclusivos de cada página personalizada.
- `assets/js/main.js`: interacciones compartidas, separadas y comentadas por funcionalidad.
- `assets/images/`: imágenes clasificadas por sección: marca, inicio, empresa, servicios, clientes, proyectos, equipo y testimonios.
- `assets/vendor/`: Bootstrap y demás dependencias externas.
- `docs/`: licencia, referencia y documentación de la plantilla original.
- `tools/validate_site.py`: revisión automática de rutas locales y estructura básica.

## Desarrollo local

No requiere compilación para visualizarse. Sirve la carpeta raíz con cualquier servidor HTTP estático y abre `index.html`.

Por ejemplo, con Python:

```powershell
python -m http.server 8000
```

Luego visita `http://localhost:8000`.

## Validación

Desde la raíz del proyecto ejecuta:

```powershell
python tools/validate_site.py
```

El validador informa si alguna página referencia un archivo local inexistente, si reaparecen rutas de la estructura anterior o si se insertan nuevos bloques `<style>` dentro del HTML.

## Convenciones de mantenimiento

- Guarda una imagen nueva dentro de la carpeta de la sección que la utiliza.
- Coloca reglas reutilizables en `assets/css/main.css` y reglas exclusivas en `assets/css/pages/`.
- Mantén el comportamiento compartido en `assets/js/main.js` y comenta cada bloque funcional, no cada línea.
- Conserva las librerías externas dentro de `assets/vendor/`; evita mezclar código propio con dependencias.
