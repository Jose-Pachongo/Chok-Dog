function abrirRecuperacion() {
    Swal.fire({
        title: "Recuperar contraseña",
        html: `
            <p>Ingresa tu correo y te enviaremos un enlace para restablecer tu contraseña.</p>
            <input type="email" id="emailRecuperacion" class="swal2-input" placeholder="Correo electrónico">
        `,
        confirmButtonText: "Enviar",
        showCancelButton: true,
        cancelButtonText: "Cancelar",
        preConfirm: () => {
            const email = document.getElementById("emailRecuperacion").value;
            if (!email) {
                Swal.showValidationMessage("Debes ingresar un correo válido.");
                return false;
            }
            return fetch("/recuperar-contrasena-ajax/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCSRFToken(),
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: `email=${encodeURIComponent(email)}`
            }).then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    Swal.fire({
                        title: "¡Correo enviado!",
                        text: "Revisa tu bandeja de entrada para restablecer tu contraseña.",
                        icon: "success",
                        confirmButtonText: "Entendido"
                    });
                } else {
                    Swal.fire({
                        title: "Error",
                        text: data.message,
                        icon: "error",
                        confirmButtonText: "Intentar de nuevo"
                    });
                }
            }).catch(() => {
                Swal.fire("Error", "Ocurrió un problema, intenta de nuevo.", "error");
            });
        }
    });
}

// Función para obtener el CSRF token desde la cookie
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length, cookie.length);
                break;
            }
        }
    }
    return cookieValue;
}
