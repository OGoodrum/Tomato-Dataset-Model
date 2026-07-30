const password = document.querySelector('input[name="psw"]');
const confirmPassword = document.querySelector('input[name="psw-repeat"]');

function validatePassword() {
    if (password.value !== confirmPassword.value) {
        confirmPassword.setCustomValidity("Passwords do not match!");
    } else {
        confirmPassword.setCustomValidity("");
    }
}

if (password && confirmPassword) {
    password.addEventListener('input', validatePassword);
    confirmPassword.addEventListener('input', validatePassword);
}