// Get the modal
var modal = document.getElementById('login_popup');


// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

const signupClick = () => {
    fetch(`/signup.html`)
    .then(res => {
        if (res.ok){
            return res.text()
        }
    }).then(htmlSnippet => {
        modal.innerHTML = htmlSnippet;
    });
}