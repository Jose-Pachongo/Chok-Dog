document.addEventListener("DOMContentLoaded", function () {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    let facturaBody = document.getElementById("factura-body");
    let totalPago = document.getElementById("total-pago");

    // 🛑 Verifica si el carrito está vacío
    if (carrito.length === 0) {
        facturaBody.innerHTML = "<tr><td colspan='4'>No hay productos en el carrito</td></tr>";
        totalPago.innerText = "Total a Pagar: $0.00";
        return;
    }

    // 🔄 Mostrar los productos en la factura
    facturaBody.innerHTML = "";
    let total = 0;

    carrito.forEach(producto => {
        let subtotal = producto.precio * producto.cantidad;
        total += subtotal;

        let fila = `
            <tr>
                <td>${producto.nombre}</td>
                <td>${producto.cantidad}</td>
                <td>$${producto.precio.toFixed(2)}</td>
                <td>$${subtotal.toFixed(2)}</td>
            </tr>
        `;
        facturaBody.innerHTML += fila;
    });

    totalPago.innerText = `Total a Pagar: $${total.toFixed(2)}`;
});
