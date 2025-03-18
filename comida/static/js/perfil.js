document.addEventListener("DOMContentLoaded", function () {
    const editProfileBtn = document.getElementById("edit-profile-btn");
    const saveProfileBtn = document.getElementById("save-profile-btn");
    const deleteBtn = document.getElementById("delete-photo-btn");
    const profilePic = document.getElementById("profile-pic");
    const profilePicInput = document.getElementById("profile-pic-input");
    const inputs = document.querySelectorAll("#profile-form input:not([type='file'])");
    const editIcon = document.querySelector(".edit-icon"); // Asegurar que seleccionamos el ícono correctamente

    // Verificar que el botón "Editar perfil" existe antes de agregar el evento
    if (editProfileBtn) {
        // Ocultar botón de eliminar foto e ícono de edición al inicio
        deleteBtn.style.display = "none";
        editIcon.style.display = "none";
        

        // Activar edición del perfil al hacer clic en "Editar perfil"
        editProfileBtn.addEventListener("click", function (event) {
            inputs.forEach(input => input.disabled = false); // Habilitar los campos
            saveProfileBtn.style.display = "block"; // Mostrar botón "Guardar cambios"
            editIcon.style.display = "block"; // Mostrar el ícono de edición de foto
            deleteBtn.style.display = "block"; // Mostrar botón "Eliminar foto"
            this.style.display = "none"; // Ocultar el botón "Editar perfil"
        });
    } else {
        console.error("El botón 'Editar perfil' no se encontró.");
    }

    // Vista previa de imagen al seleccionar un nuevo archivo
    if (profilePicInput) {
        profilePicInput.addEventListener("change", function (event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    profilePic.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Eliminar foto de perfil
    if (deleteBtn) {
        deleteBtn.addEventListener("click", function () {
            if (confirm("¿Estás seguro de que deseas eliminar tu foto de perfil?")) {
                fetch("/eliminar-foto/", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": getCSRFToken(),
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        profilePic.src = "/static/img/perfil.webp"; // Reemplaza con la imagen predeterminada
                        alert("Foto eliminada correctamente.");
                    } else {
                        alert("Error al eliminar la foto.");
                    }
                })
                .catch(error => console.error("Error:", error));
            }
        });
    }

    function getCSRFToken() {
        return document.querySelector("[name=csrfmiddlewaretoken]").value;
    }
});
document.addEventListener("DOMContentLoaded", function () {
    const profilePic = document.getElementById("profile-pic");
    const modal = document.getElementById("modal-profile");
    const modalImg = document.getElementById("modal-img");
    const closeBtn = document.querySelector(".close");

    // Mostrar modal con la imagen ampliada
    profilePic.addEventListener("click", function () {
        modal.style.display = "flex";
        modalImg.src = this.src;
    });

    // Cerrar modal
    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Cerrar modal si se hace clic fuera de la imagen
    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
});
