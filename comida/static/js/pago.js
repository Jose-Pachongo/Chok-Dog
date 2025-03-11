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
            const direccion = document.getElementById("direccion").value.trim(); // ✅ Captura la dirección
            const metodoPago = document.querySelector("input[name='metodo_pago']:checked");
            const comprobante = document.getElementById("comprobante").files[0];

            if (!nombre || !email || !telefono || !direccion || !metodoPago || !comprobante) {
                Swal.fire("Error", "Todos los campos son obligatorios", "error");
                return;
            }

            const formData = new FormData();
            formData.append("nombre", nombre);
            formData.append("email", email);
            formData.append("telefono", telefono);
            formData.append("direccion", direccion); // ✅ Agrega la dirección
            formData.append("metodo_pago", metodoPago.value);
            formData.append("comprobante", comprobante);
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
                        window.location.href = "/productos/"; // Reemplaza con la URL real de tus productos
                    });
                    
                } else {
                    Swal.fire({
                        icon: "error",
                        title: "Error",
                        text: data.error || "Ocurrió un error inesperado.",
                        confirmButtonColor: "#6c5ce7"
                    });
                }
            })
            .catch(error => {
                console.error("Error en el pago:", error);
                Swal.fire("Error", "Hubo un problema al procesar el pedido", "error");
            });
        });
    } else {
        console.warn("⚠️ No se encontró el formulario de pago.");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const metodoPagoRadios = document.querySelectorAll("input[name='metodo_pago']");
    const nequiContainer = document.getElementById("nequi-container");
    const daviplataContainer = document.getElementById("daviplata-container");

    metodoPagoRadios.forEach(radio => {
        radio.addEventListener("change", function () {
            if (this.value === "nequi") {
                nequiContainer.style.display = "block";
                daviplataContainer.style.display = "none";
            } else if (this.value === "daviplata") {
                nequiContainer.style.display = "none";
                daviplataContainer.style.display = "block";
            }
        });
    });
});

