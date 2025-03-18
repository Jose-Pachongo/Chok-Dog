document.addEventListener("DOMContentLoaded", function () {
    const fechaInput = document.getElementById("fecha");
    const horaInput = document.getElementById("hora");

    // Restringe la selección de fechas anteriores a la actual
    const hoy = new Date().toISOString().split("T")[0];
    fechaInput.setAttribute("min", hoy);

    // Restringe la selección de horas fuera del rango 17:00 - 23:00
    function validarHora() {
        if (!horaInput.value) return; // Evita errores si el campo está vacío

        let horaSeleccionada = parseInt(horaInput.value.split(":")[0]);

        if (horaSeleccionada < 17 || horaSeleccionada > 23) {
            Swal.fire({
                icon: "error",
                title: "Hora no válida",
                text: "Por favor, selecciona una hora entre las 17:00 y las 23:00.",
                confirmButtonText: "Entendido"
            });
            horaInput.value = ""; // Borra la hora inválida
        }
    }

    // Validar fecha para evitar errores de evento no definido
    function validarFecha() {
        if (fechaInput.value < hoy) {
            fechaInput.value = hoy;
        }
    }

    fechaInput.addEventListener("change", validarFecha);
    horaInput.addEventListener("change", validarHora); // Usa 'change' para evitar errores
});

