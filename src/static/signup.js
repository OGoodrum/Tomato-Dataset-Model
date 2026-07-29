const password = document.getElementsByName("psw");
const confirmPassword = document.getElementsByName("psw-repeat");

function validatePassword(){
    if(password.value !== confirmPassword.value){
        confirmPassword.setCustomValidity("Password do not mathch!");
    } else {
        confirmPassword.setCustomValidity("");
    }
}

password.addEventListener("change", validatePassword);
confirmPassword.addEventListener("keyup", validatePassword);