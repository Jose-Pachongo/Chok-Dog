document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript cargado correctamente.");

    let profileBtn = document.getElementById("profileBtn");
    let dropdown = document.getElementById("profileDropdown");

    if (profileBtn && dropdown) {
        profileBtn.addEventListener("click", function (e) {
            e.stopPropagation(); // Evita que el evento se propague
            dropdown.classList.toggle("active");
        });

        // Cierra el menú si se hace clic fuera de él
        document.addEventListener("click", function (event) {
            if (!profileBtn.contains(event.target) && !dropdown.contains(event.target)) {
                dropdown.classList.remove("active");
            }
        });
    }
});