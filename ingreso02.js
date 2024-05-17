const $submit = document.getElementById("submit")
const $email = document.getElementById("email")
const $contraseña = document.getElementById("contraseña")

function validateInputs(){
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    const contraseñaRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,}$/;

    if($email.value === ""){
        alert("El campo se encuentra vacío");
        return false;
    }
    if($contraseña.value === ""){
        alert("El campo se encuentra vacío");
        return false;
    }
    if(!emailRegex.test($email.value)){
        alert("No cumple con las condiciones");
        $email.style.border = "1px solid red";
        return false;
    }
    if(!contraseñaRegex.test($contraseña.value)){
        alert("No cumple con las condiciones");
        $contraseña.style.border = "1px solid red";
        return false;
    }
    return true
}

document.addEventListener("click", (e) => {
    if(e.target === $submit) {
        e.preventDefault();
        validateInputs();
    }
});