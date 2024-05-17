//form login

const $submit = document.getElementById("submit");
const $email = document.getElementById("email");
const $contraseña = document.getElementById("contraseña");

function validateInputs() {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const contraseñaRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/;

    $email.style.border = "";
    $contraseña.style.border = "";

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