// Get the modal
var modal = document.getElementById('login_popup');

document.addEventListener('submit', function (e) {
    if (e.target && e.target.classList.contains('modal-content')) {
        e.preventDefault();
        const formData = new FormData(e.target);

        fetch('/api/login', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                window.location.reload(); // Successfully logged in
                console.log("succes");
            } else {
                alert(data.message || 'Login failed');
            }
        });
    }
});
