//comentarios y noticias admin

document.addEventListener('DOMContentLoaded', function() {
    var dropdown = document.querySelector('.dropdownTitle');
    dropdown.addEventListener('click', function() {
        var dropdownContent = document.querySelector('.dropdownCont');
        if (dropdownContent.style.display === "block") {
            dropdownContent.style.display = "none";
        } else {
            dropdownContent.style.display = "block";
        }
    });

    window.onclick = function(event) {
        if (!event.target.matches('.dropdownTitle, .dropdownTitle *')) {
            var dropdowns = document.getElementsByClassName("dropdownCont");
            for (var i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.style.display === "block") {
                    openDropdown.style.display = "none";
                }
            }
        }
    }
});

// advertencia crear noticia sin usuario

document.addEventListener("DOMContentLoaded", function () {
    const crearNoticiaBtn = document.querySelector('.headerUserCont a[href="noticia.html"]');

    if (crearNoticiaBtn) {
        crearNoticiaBtn.addEventListener("click", function (e) {
            const logueado = localStorage.getItem("logueado");
            if (logueado !== "true") {
                e.preventDefault();
                alert("Debes iniciar sesión para crear una noticia.");
                window.location.href = "login.html";
            }
        });
    }
});