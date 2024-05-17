const $submit = document.getElementById("submit")
const $nombre = document.getElementById("nombre")
const $apellido = document.getElementById("apellido")
const $categoria = document.getElementById("categoría")
const $titulo = document.getElementById("titulo")
const $subtitulo = document.getElementById("subtitulo")
const $cuerpo = document.getElementById("cuerpo")
const $imagen = document.getElementById("imagen")

function validateInputs(){
    const nombreRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,24}$/;
    const apellidoRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,32}$/;
    const categoriaRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{4,32}$/;
    const tituloRegex = /^.{1,100}$/;
    const subtituloRegex = /^.{1,100}$/;
    const cuerpoRegex = /.*/;
    
    if($nombre.value === ""){
        alert("El campo se encuentra vacío");
        return false;
    }
    if($apellido.value === ""){
        alert("El campo se encuentra vacío");
        return false;
    }
    if($categoria.value === ""){
        alert("El campo se encuentra vacío");
        return false;
    }
    if($titulo.value === ""){
        alert("El campo se encuentra vacío");
        return false;
    }
    if($subtitulo.value === ""){
        alert("El campo se encuentra vacío");
        return false;
    }
    if($cuerpo.value === ""){
        alert("El campo se encuentra vacío");
        return false;
    }
    if($imagen.src){
        alert("Imagen colocada");
    } else {
        alert("Debe colocar una imagen");
        return false;
    }
    if(!nombreRegex.test($nombre.value)){
        alert("No cumple con las condiciones");
        $nombre.style.border = "1px solid red";
        return false;
    }
    if(!apellidoRegex.test($apellido.value)){
        alert("No cumple con las condiciones");
        $apellido.style.border = "1px solid red";
        return false;
    }
    if(!categoriaRegex.test($categoria.value)){
        alert("No cumple con las condiciones");
        $categoria.style.border = "1px solid red";
        return false;
    }
    if(!tituloRegex.test($titulo.value)){
        alert("No cumple con las condiciones");
        $titulo.style.border = "1px solid red";
        return false;
    }
    if(!subtituloRegex.test($subtitulo.value)){
        alert("No cumple con las condiciones");
        $subtitulo.style.border = "1px solid red";
        return false;
    }
    if(!cuerpoRegex.test($cuerpo.value)){
        alert("No cumple con las condiciones");
        $cuerpo.style.border = "1px solid red";
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