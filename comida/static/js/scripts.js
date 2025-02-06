function loguear() {
    let user = document.getElementById("usuario").value;
    let pass = document.getElementById("clave").value;

    const usuarios = {
        "1062077111":"111",
        "1062077222":"222",
        "1062077333":"333"
    }; 

    if (usuarios[user] && usuarios[user] === pass) {
        window.location = "home.html";
        } else {
            alert("Usuario o contraseña incorrectos");
        }

}

