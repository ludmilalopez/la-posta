//form login


const submit = document.getElementsByClassName('formSubmit')[0];
const $email = document.getElementById("email");
const $contraseña = document.getElementById("contrasena");

const validateEmail = (email) => {
  return email.match(
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
};

submit.onclick= (event) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    // const contraseñaRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/;

    $email.style.border = "";
    $contraseña.style.border = "";

    if ($email.value === "") {
        event.preventDefault();
        alert("El campo de email se encuentra vacío");
        $email.style.border = "1px solid red";
        return false;
    }
    if ($contraseña.value === "") {
        event.preventDefault();
        alert("El campo de contraseña se encuentra vacío");
        $contraseña.style.border = "1px solid red";
        return false;
    }
    if (!emailRegex.test($email.value)) {
        event.preventDefault();
        alert("El email no cumple con las condiciones");
        $email.style.border = "1px solid red";
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