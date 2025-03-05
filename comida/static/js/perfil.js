document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("passwordModal");
    const openModalBtn = document.getElementById("openModalBtn");
    const closeModal = document.querySelector(".close");

    // Abrir el modal al hacer clic en "Cambiar contraseña"
    openModalBtn.addEventListener("click", function () {
        modal.style.display = "flex";
    });

    // Cerrar el modal al hacer clic en la "X"
    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    });

    // Cerrar el modal si el usuario hace clic fuera de la caja
    window.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
        }
    });
});