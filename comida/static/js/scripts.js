function loguear() {
    let user = document.getElementById("usuario").value;
    let pass = document.getElementById("clave").value;

    if (!user || !pass) {
        alert("Por favor, ingrese tanto el usuario como la contraseña.");
        return;
    }

    const usuarios = {
        "1062077111":"111",
        "1062077222":"222",
        "1062077333":"333"
    };

    if (usuarios[user] && usuarios[user] === pass) {
        window.location = "pagina"; // O la URL correcta
    } else {
        alert("Usuario o contraseña incorrectos");
    }
}
