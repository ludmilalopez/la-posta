//comentarios y noticias admin

//comentariosAdm.html

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

//noticiasAdm.html

