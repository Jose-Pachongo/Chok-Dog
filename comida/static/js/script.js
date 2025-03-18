document.addEventListener("DOMContentLoaded", function () {
    console.log("JavaScript cargado correctamente.");

    let profileBtn = document.getElementById("profileBtn");
    let dropdown = document.getElementById("profileDropdown");

    if (profileBtn && dropdown) {
        profileBtn.addEventListener("click", function (e) {
            e.stopPropagation(); // 
            dropdown.classList.toggle("active");
        });

        
        document.addEventListener("click", function (event) {
            if (!profileBtn.contains(event.target) && !dropdown.contains(event.target)) {
                dropdown.classList.remove("active");
            }
        });
    }
});

