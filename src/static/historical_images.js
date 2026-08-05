
const imageArea = document.querySelector('.imageArea');

const imageData = window.imageData || [];

function updateImageArea() {
    let newInnerHTML = '';
    imageData.forEach((item) => {
        if (item.image_url) {
            const formattedTime = new Date(item.created_at).toLocaleString();
            newInnerHTML += `
            <li class="image-container">
                <a href="${item.image_url}" target="_blank">
                    <img src="${item.image_url}" width="640" height="480" />
                    <div class="timestamp">${formattedTime}</div>
                </a>
            </li>
            `;
        }
    });

    imageArea.innerHTML = newInnerHTML;
}

updateImageArea();
