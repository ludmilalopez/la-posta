//form registrarse

const $submit = document.getElementById("submit");
const $nombre = document.getElementById("nombre");
const $apellido = document.getElementById("apellido");
const $usuario = document.getElementById("usuario");
const $email = document.getElementById("email");
const $contraseña = document.getElementById("psw");
const $repetircontraseña = document.getElementById("psw-repeat");

submit.onclick= (event) => {
    const nombreRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,24}$/;
    const apellidoRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,32}$/;
    const usuarioRegex = /^[a-zA-Z0-9]{4,16}$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const contraseñaRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/;

    $nombre.style.border = "";
    $apellido.style.border = "";
    $usuario.style.border = "";
    $email.style.border = "";
    $contraseña.style.border = "";
    $repetircontraseña.style.border = "";

    if ($nombre.value === "") {
        alert("El campo de nombre se encuentra vacío");
        $nombre.style.border = "1px solid red";
        return false;
    }
    if ($apellido.value === "") {
        alert("El campo de apellido se encuentra vacío");
        $apellido.style.border = "1px solid red";
        return false;
    }
    if ($usuario.value === "") {
        alert("El campo de usuario se encuentra vacío");
        $usuario.style.border = "1px solid red";
        return false;
    }
    if ($email.value === "") {
        alert("El campo de email se encuentra vacío");
        $email.style.border = "1px solid red";
        return false;
    }
    if ($contraseña.value === "") {
        alert("El campo de contraseña se encuentra vacío");
        $contraseña.style.border = "1px solid red";
        return false;
    }
    if ($repetircontraseña.value === "") {
        alert("El campo de repetir contraseña se encuentra vacío");
        $repetircontraseña.style.border = "1px solid red";
        return false;
    }
    if (!nombreRegex.test($nombre.value)) {
        alert("El nombre no cumple con las condiciones");
        $nombre.style.border = "1px solid red";
        return false;
    }
    if (!apellidoRegex.test($apellido.value)) {
        alert("El apellido no cumple con las condiciones");
        $apellido.style.border = "1px solid red";
        return false;
    }
    if (!usuarioRegex.test($usuario.value)) {
        alert("El usuario no cumple con las condiciones");
        $usuario.style.border = "1px solid red";
        return false;
    }
    if (!emailRegex.test($email.value)) {
        alert("El email no cumple con las condiciones");
        $email.style.border = "1px solid red";
        return false;
    }
    if (!contraseñaRegex.test($contraseña.value)) {
        alert("La contraseña no cumple con las condiciones");
        $contraseña.style.border = "1px solid red";
        return false;
    }
    return true;
}

$submit.addEventListener("click", (e) => {
    e.preventDefault();
    if (validateInputs()) {
        console.log("Formulario enviado correctamente");
    }
});