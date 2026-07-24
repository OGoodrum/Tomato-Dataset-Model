// Get the modal
var modal = document.getElementById('login_popup');

// Imediately load in the login page
const load_login = () => {
    fetch(`../templates/login.html`)
    .then(res => {
        if (res.ok){
            return res.text()
        }
    }).then(htmlSnippet => {
        modal.innerHTML = htmlSnippet;
    });
};

load_login();


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}