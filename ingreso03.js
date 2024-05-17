const $submit = document.getElementById("submit")
const $email = document.getElementById("email")
const $contraseña = document.getElementById("contraseña")
const $repetircontraseña = document.getElementById("repetircontraseña")

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
    if($repetircontraseña.value === ""){
        alert("El campo se encuentra vacío");
        return false;
    }
    if(!emailRegex.test($email.value)){
        alert("No cumple con las condiciones del email");
        $email.style.border = "1px solid red";
        return false;
    }
    if(!contraseñaRegex.test($contraseña.value)){
        alert("No cumple con las condiciones de la contraseña");
        $contraseña.style.border = "1px solid red"
        return false;
    }
    if($repetircontraseña.value != $contraseña.value){
        alert("Revise que la contraseña coincida con la repetida");
        $repetircontraseña.style.border = "1px solid red"
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
