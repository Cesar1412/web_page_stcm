(function ($) {
    "use strict";

    // Cargador inicial: oculta el indicador cuando el documento ya está listo.
    const hideSpinner = function () {
        window.setTimeout(function () {
            $("#spinner").removeClass("show");
        }, 1);
    };
    hideSpinner();

    // Animaciones de entrada: activa los elementos configurados con WOW.js.
    if (typeof WOW !== "undefined") {
        new WOW().init();
    }

    // Navegación durante el desplazamiento: añade profundidad y controla el botón de retorno.
    const $window = $(window);
    const $navbar = $(".sticky-top");
    const $backToTop = $(".back-to-top");

    $window.on("scroll", function () {
        const hasScrolled = $window.scrollTop() > 300;
        $navbar.toggleClass("shadow-sm", hasScrolled);
        hasScrolled ? $backToTop.fadeIn("slow") : $backToTop.fadeOut("slow");
    });

    $backToTop.on("click", function (event) {
        event.preventDefault();
        $("html, body").animate({ scrollTop: 0 }, 1500, "swing");
    });
})(jQuery);
