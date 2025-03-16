document.addEventListener("DOMContentLoaded", function () {
    let pestañaActiva = localStorage.getItem("pestañaActiva");

    // Si no hay pestaña activa guardada, se selecciona la de compras por defecto
    if (!pestañaActiva) {
        pestañaActiva = 'compras';  // Por defecto es 'compras'
    }

    // Mostrar la pestaña activa
    showTab(pestañaActiva);
});

function showTab(tab) {
    // Primero, desactivar todas las pestañas y contenidos
    document.querySelectorAll('.content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));

    // Activar la pestaña correspondiente
    document.getElementById(tab).classList.add('active');
    document.querySelector(`.tab-container .tab[onclick="showTab('${tab}')"]`).classList.add('active');

    // Guardar la pestaña activa en localStorage
    localStorage.setItem("pestañaActiva", tab);
}





document.addEventListener("DOMContentLoaded", function () {
    restaurarReservasAlCargar();
});

function eliminarReserva(reservaId) {
    if (confirm("¿Seguro que deseas eliminar esta reserva?")) {
        // Guardar en LocalStorage antes de eliminar
        let reservasEliminadas = JSON.parse(localStorage.getItem("reservasEliminadas")) || [];
        let fila = document.getElementById(`reserva-${reservaId}`);
        if (fila) {
            reservasEliminadas.push(fila.outerHTML); // Guardamos la fila completa
            localStorage.setItem("reservasEliminadas", JSON.stringify(reservasEliminadas));
            fila.remove(); // Eliminar visualmente la reserva
        }
    }
}

function restaurarReservas() {
    if (confirm("¿Deseas restaurar todas las reservas eliminadas?")) {
        let reservasEliminadas = JSON.parse(localStorage.getItem("reservasEliminadas")) || [];
        let reservasLista = document.getElementById("reservas-lista");

        reservasEliminadas.forEach(html => {
            let nuevaFila = document.createElement("tr");
            nuevaFila.innerHTML = html;
            reservasLista.appendChild(nuevaFila);
        });

        localStorage.removeItem("reservasEliminadas"); // Limpiar después de restaurar
        alert("Reservas restauradas correctamente.");
    }
}

function restaurarReservasAlCargar() {
    let reservasEliminadas = JSON.parse(localStorage.getItem("reservasEliminadas")) || [];
    if (reservasEliminadas.length > 0) {
        let reservasLista = document.getElementById("reservas-lista");
        reservasEliminadas.forEach(html => {
            let nuevaFila = document.createElement("tr");
            nuevaFila.innerHTML = html;
            reservasLista.appendChild(nuevaFila);
        });
    }
}

function mostrarTabla(tabla) {
    document.getElementById("tabla-compras").style.display = (tabla === "compras") ? "table" : "none";
    document.getElementById("tabla-reservas").style.display = (tabla === "reservas") ? "table" : "none";

    // Resaltar el botón activo
    document.getElementById("btn-compras").classList.toggle("activo", tabla === "compras");
    document.getElementById("btn-reservas").classList.toggle("activo", tabla === "reservas");

    // Guardar la última pestaña en localStorage
    localStorage.setItem("pestañaActiva", tabla);
}
// Función para eliminar y guardar en localStorage
function confirmarEliminacionPedido(pedidoId) {
    if (confirm("¿Estás seguro de que quieres eliminar este pedido? Esta acción no se puede deshacer.")) {
        let fila = document.getElementById("pedido-" + pedidoId);
        if (fila) {
            fila.style.display = "none"; // Oculta la fila
            fila.classList.add("pedido-oculto");

            // Guardar en localStorage
            let pedidosEliminados = JSON.parse(localStorage.getItem("pedidosEliminados")) || [];
            if (!pedidosEliminados.includes(pedidoId)) {
                pedidosEliminados.push(pedidoId);
            }
            localStorage.setItem("pedidosEliminados", JSON.stringify(pedidosEliminados));
        }
    }
}


// Restaurar pedidos ocultos
function restaurarPedidos() {
    if (confirm("¿Deseas restaurar todos los pedidos eliminados?")) {
        let pedidosEliminados = JSON.parse(localStorage.getItem("pedidosEliminados")) || [];

        pedidosEliminados.forEach(pedidoId => {
            let fila = document.getElementById("pedido-" + pedidoId);
            if (fila) {
                fila.style.display = "table-row"; // Mostrar de nuevo la fila
                fila.classList.remove("pedido-oculto");
            }
        });

        // Limpiar LocalStorage después de restaurar
        localStorage.removeItem("pedidosEliminados");

        alert("Pedidos restaurados correctamente.");
    }
}


// Al cargar la página, ocultar los pedidos que fueron eliminados
document.addEventListener("DOMContentLoaded", function () {
    let pedidosEliminados = JSON.parse(localStorage.getItem("pedidosEliminados")) || [];
    pedidosEliminados.forEach(pedidoId => {
        let fila = document.getElementById("pedido-" + pedidoId);
        if (fila) {
            fila.style.display = "none"; // Mantener oculto después de recargar
            fila.classList.add("pedido-oculto");
        }
    });
});


function showTab(tab) {
    document.querySelectorAll('.content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(el => el.classList.remove('active'));
    document.getElementById(tab).classList.add('active');
    document.querySelector(`.tab-container .tab[onclick="showTab('${tab}')"]`).classList.add('active');
}

function cambiarEstado(id, nuevoEstado) {
    document.getElementById(id).textContent = nuevoEstado;
}




function confirmarEliminacionReserva(reservaId) {
    if (confirm("¿Estás seguro de que quieres eliminar esta reserva?")) {
        window.location.href = `/eliminar_reserva/${reservaId}/`;
    }
}
function confirmarCancelacionPedido(pedidoId) {
if (confirm("¿Estás seguro de que quieres cancelar este pedido? Esta acción no se puede deshacer.")) {
    window.location.href = `/cancelar_pedido/${pedidoId}/`;
}
}

fetch('/historial/reservas/')
    .then(response => response.json())  // Intentar convertir la respuesta a JSON
    .then(data => {
        console.log("Reservas obtenidas:", data);  // Verificar los datos recibidos
    })
    .catch(error => console.error("Error al obtener reservas:", error));
