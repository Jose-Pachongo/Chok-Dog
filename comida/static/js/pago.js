document.addEventListener("DOMContentLoaded", function () {
    const carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    const carritoBody = document.getElementById("carrito-body");
    const totalPago = document.getElementById("total-pago");

    if (!carritoBody) {
        console.warn("⚠️ No se encontró el elemento con ID 'carrito-body'");
        return;
    }

    // Limpiar contenido previo
    carritoBody.innerHTML = "";
    let total = 0;

    carrito.forEach(item => {
        let subtotal = item.precio * item.cantidad;
        total += subtotal;

        let row = document.createElement("tr");
        row.innerHTML = `
            <td>${item.nombre}</td>
            <td>${item.cantidad}</td>
            <td>$${item.precio.toLocaleString()}</td>
            <td>$${subtotal.toLocaleString()}</td>
        `;
        carritoBody.appendChild(row);
    });

    totalPago.textContent = `Total: $${total.toLocaleString()}`;

    // Manejo del formulario de pago
    const paymentForm = document.getElementById("payment-form");

    if (paymentForm) {
        paymentForm.addEventListener("submit", function (e) {
            e.preventDefault();

            const nombre = document.getElementById("nombre").value.trim();
            const email = document.getElementById("email").value.trim();
            const telefono = document.getElementById("telefono").value.trim();
            const direccion = document.getElementById("direccion").value.trim();
            const metodoPago = document.querySelector("input[name='metodo_pago']:checked") || { value: "no seleccionado" };
            const comprobante = document.getElementById("comprobante").files[0];

            // Referencia al botón de envío
            let submitButton = document.getElementById("submit-button");

            // Validaciones
            if (!nombre || !email || !telefono || !direccion || !metodoPago) {
                Swal.fire("Error", "Todos los campos son obligatorios", "error");
                return;
            }

            if (metodoPago.value !== "contra_entrega" && !comprobante) {
                Swal.fire("Error", "Debes subir un comprobante de pago", "error");
                return;
            }

            // Deshabilitar el botón para evitar múltiples envíos
            submitButton.disabled = true;
            submitButton.innerText = "Procesando...";

            const formData = new FormData();
            formData.append("nombre", nombre);
            formData.append("email", email);
            formData.append("telefono", telefono);
            formData.append("direccion", direccion);
            formData.append("metodo_pago", metodoPago.value);
            if (comprobante) formData.append("comprobante", comprobante);
            formData.append("productos", JSON.stringify(carrito));
            formData.append("total", total);

            const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
            if (!csrfToken) {
                console.error("⚠️ No se encontró el CSRF token en el formulario.");
                return;
            }

            fetch("/procesar_pedido/", {
                method: "POST",
                body: formData,
                headers: {
                    "X-CSRFToken": csrfToken.value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.mensaje) {
                    Swal.fire({
                        icon: "success",
                        title: "¡Éxito!",
                        text: data.mensaje,
                        confirmButtonColor: "#6c5ce7"
                    }).then(() => {
                        localStorage.removeItem("carrito");
                        window.location.href = "/productos/"; // Redirige a productos
                    });

                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Error",
                        text: data.error || "Ocurrió un error inesperado.",
                        confirmButtonColor: "#6c5ce7"
                    });
                    // Reactivar el botón en caso de error
                    submitButton.disabled = false;
                    submitButton.innerText = "Confirmar Pedido";
                }
            })
            .catch(error => {
                console.error("Error en el pago:", error);
                Swal.fire("Error", "Hubo un problema al procesar el pedido", "error");
                // Reactivar el botón en caso de error
                submitButton.disabled = false;
                submitButton.innerText = "Confirmar Pedido";
            });
        });
    } else {
        console.warn("⚠️ No se encontró el formulario de pago.");
    }
});

// Manejo de selección de método de pago
document.querySelectorAll('input[name="metodo_pago"]').forEach((input) => {
    input.addEventListener("change", function () {
        // Verificar si el usuario está seleccionando la misma opción para desmarcarla
        if (this.dataset.selected === "true") {
            this.checked = false;
            this.dataset.selected = "false";
            resetPago();
            return;
        }

        // Marcar la opción actual como seleccionada y resetear las demás
        document.querySelectorAll('input[name="metodo_pago"]').forEach((otherInput) => {
            otherInput.dataset.selected = "false";
        });
        this.dataset.selected = "true";

        // Mostrar QR según el método de pago seleccionado
        document.getElementById("nequi-container").style.display = this.value === "nequi" ? "block" : "none";
        document.getElementById("daviplata-container").style.display = this.value === "daviplata" ? "block" : "none";

        // Ocultar comprobante si es pago contra entrega
        let comprobanteSection = document.getElementById("comprobante-section");
        if (this.value === "contra_entrega") {
            comprobanteSection.style.display = "none";
            document.getElementById("comprobante").removeAttribute("required");
        } else {
            comprobanteSection.style.display = "block";
            document.getElementById("comprobante").setAttribute("required", "true");
        }
    });
});

// Función para resetear la selección de pago
function resetPago() {
    document.querySelectorAll('input[name="metodo_pago"]').forEach((input) => {
        input.checked = false;
    });

    document.getElementById("nequi-container").style.display = "none";
    document.getElementById("daviplata-container").style.display = "none";
    document.getElementById("comprobante-section").style.display = "block";
    document.getElementById("comprobante").setAttribute("required", "true");
}

// Función para manejar la navegación entre pasos de la pasarela de pago
function mostrarPaso(paso) {
    // Ocultar todos los pasos
    document.querySelectorAll('.paso').forEach(el => el.style.display = 'none');
    
    // Mostrar solo el paso actual
    document.getElementById('paso-' + paso).style.display = 'block';

    // Actualizar barra de progreso
    document.querySelectorAll('.step').forEach(el => el.classList.remove('active'));
    document.getElementById('step-' + paso).classList.add('active');
}
