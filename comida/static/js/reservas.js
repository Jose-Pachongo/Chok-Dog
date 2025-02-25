document.addEventListener("DOMContentLoaded", function() {
    var messagesScript = document.getElementById("django-messages");
    if (messagesScript) {
      try {
        var djangoMessages = JSON.parse(messagesScript.textContent);
        djangoMessages.forEach(function(msg) {
          Swal.fire({
            title: msg.tags.includes('error') ? "Error" : "Información",
            text: msg.message,
            icon: msg.tags.includes('error') ? "error" : "success",
            confirmButtonColor: msg.tags.includes('error') ? "#d33" : "#3085d6"
          });
        });
      } catch (e) {
        console.error("Error al parsear los mensajes de Django:", e);
      }
    }
  });


$(document).ready(function() {
    let today = new Date().toISOString().split('T')[0];
    $('#fecha').attr('min', today);

   
    $('#hora').on('input', function() {
        let horaSeleccionada = $(this).val();
        if (horaSeleccionada < "17:00" || horaSeleccionada > "23:00") {
            alert("Por favor, selecciona una hora entre 17:00 y 23:00.");
            $(this).val('');
        }
    });


    $('#fecha, #hora').on('change', function() {
        let fecha = $('#fecha').val();
        let hora = $('#hora').val();
        if (fecha && hora) {
            $.ajax({
                url: '{% url "obtener_mesas_disponibles" %}',
                data: {
                    'fecha': fecha,
                    'hora': hora
                },
                success: function(data) {
                    let mesaSelect = $('#mesa');
                    mesaSelect.empty();
                    if (data.mesas_disponibles.length > 0) {
                        data.mesas_disponibles.forEach(function(mesa) {
                            let option = $('<option></option>')
                                .val(mesa.id)
                                .text('Mesa ' + mesa.numero)
                                .css('color', mesa.disponible ? 'green' : 'red');
                            if (!mesa.disponible) {
                                option.prop('disabled', true);
                            }
                            mesaSelect.append(option);
                        });
                    } else {
                        let option = $('<option></option>')
                            .text('No hay mesas disponibles')
                            .prop('disabled', true);
                        mesaSelect.append(option);
                    }
                }
            });
        }
    });
});
