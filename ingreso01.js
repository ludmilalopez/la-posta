//form crear noticia

const $submit = document.getElementById("submit");
const $nombre = document.getElementById("nombre");
const $apellido = document.getElementById("apellido");
const $categoria = document.getElementById("categoria");
const $titulo = document.getElementById("titulo");
const $subtitulo = document.getElementById("subtitulo");
const $cuerpo = document.getElementById("cuerpo");
const $imagen = document.getElementById("imagen");

submit.onclick= (event) => {
    const nombreRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,24}$/;
    const apellidoRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{2,32}$/;
    const categoriaRegex = /^[a-zA-ZáéíóúÁÉÍÓÚüÜ]{4,32}$/;
    const tituloRegex = /^.{1,100}$/;
    const subtituloRegex = /^.{1,100}$/;
    const cuerpoRegex = /.*/;

    $nombre.style.border = "";
    $apellido.style.border = "";
    $categoria.style.border = "";
    $titulo.style.border = "";
    $subtitulo.style.border = "";
    $cuerpo.style.border = "";

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
    if ($categoria.value === "") {
        alert("El campo de categoría se encuentra vacío");
        $categoria.style.border = "1px solid red";
        return false;
    }
    if ($titulo.value === "") {
        alert("El campo de título se encuentra vacío");
        $titulo.style.border = "1px solid red";
        return false;
    }
    if ($subtitulo.value === "") {
        alert("El campo de subtítulo se encuentra vacío");
        $subtitulo.style.border = "1px solid red";
        return false;
    }
    if ($cuerpo.value === "") {
        alert("El campo de cuerpo se encuentra vacío");
        $cuerpo.style.border = "1px solid red";
        return false;
    }
    if ($imagen.files.length === 0) {
        alert("Debe colocar una imagen");
        $imagen.style.border = "1px solid red";
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
    if (!categoriaRegex.test($categoria.value)) {
        alert("La categoría no cumple con las condiciones");
        $categoria.style.border = "1px solid red";
        return false;
    }
    if (!tituloRegex.test($titulo.value)) {
        alert("El título no cumple con las condiciones");
        $titulo.style.border = "1px solid red";
        return false;
    }
    if (!subtituloRegex.test($subtitulo.value)) {
        alert("El subtítulo no cumple con las condiciones");
        $subtitulo.style.border = "1px solid red";
        return false;
    }
    if (!cuerpoRegex.test($cuerpo.value)) {
        alert("El cuerpo no cumple con las condiciones");
        $cuerpo.style.border = "1px solid red";
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
