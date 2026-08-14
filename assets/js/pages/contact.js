(function () {
    "use strict";

    const contactForm = document.getElementById("contactForm");
    if (!contactForm) {
        return;
    }

    // Envío del formulario: evita recargar la página y comunica la solicitud a FormSubmit.
    contactForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const submitButton = contactForm.querySelector('button[type="submit"]');
        const originalText = submitButton.innerHTML;
        submitButton.disabled = true;
        submitButton.innerHTML = "Enviando...";

        try {
            const response = await fetch("https://formsubmit.co/ajax/administracion2@stcmperusac.pe", {
                method: "POST",
                body: new FormData(contactForm),
                headers: { Accept: "application/json" }
            });
            const result = await response.json();

            if (!response.ok || result.success === false || result.success === "false") {
                throw new Error("FormSubmit rechazó la solicitud.");
            }

            window.alert("¡Solicitud enviada correctamente! Te contactaremos pronto.");
            contactForm.reset();
        } catch (error) {
            window.alert("Hubo un error al enviar tu solicitud. Inténtalo nuevamente.");
        } finally {
            submitButton.disabled = false;
            submitButton.innerHTML = originalText;
        }
    });
})();
