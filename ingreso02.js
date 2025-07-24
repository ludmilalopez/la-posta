// form login

const submit = document.getElementsByClassName('formSubmit')[0];
const $email = document.getElementById("email");
const $contraseña = document.getElementById("contrasena");

const validateEmail = (email) => {
  return email.match(
    /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
  );
};

const adminEmails = [
  "brunozarco@uca.edu.ar",
  "conradoclementi@uca.edu.ar",
  "ivankammerman@uca.edu.ar",
  "nicolasalbornoz@uca.edu.ar"
];

submit.addEventListener("click", (event) => {
  event.preventDefault();

  $email.style.border = "";
  $contraseña.style.border = "";

  if ($email.value === "") {
    alert("El campo de email se encuentra vacío");
    $email.style.border = "1px solid red";
    return;
  }

  if ($contraseña.value === "") {
    alert("El campo de contraseña se encuentra vacío");
    $contraseña.style.border = "1px solid red";
    return;
  }

  if (!validateEmail($email.value)) {
    alert("El email no cumple con las condiciones");
    $email.style.border = "1px solid red";
    return;
  }

  const emailLower = $email.value.toLowerCase();
  if (adminEmails.includes(emailLower)) {
    window.location.href = "mainAdm.html";
  } else {
    window.location.href = "mainLog.html";
  }
});