const cameraList = document.querySelector('.cameraList');

let cameraFeeds = ["https://drums-radiation-promotion-mai.trycloudflare.com/video_feed"];

function updateCameraFeeds() {
    let newInnerHTML = '';
    cameraFeeds.forEach((feed, index) => {
        newInnerHTML += `
        <li class="stream-container"><img src=${feed} width="640" height="480" /></li>
        `
    });

    cameraList.innerHTML = newInnerHTML;
}

updateCameraFeeds();