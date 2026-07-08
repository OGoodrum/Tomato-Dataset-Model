const cameraList = document.querySelector('.cameraList');

let cameraFeeds = ["https://actions-commands-gore-motorcycle.trycloudflare.com/video_feed"];

function updateCameraFeeds() {
    let newInnerHTML = '';
    cameraFeeds.forEach((feed, index) => {
        newInnerHRML += `
        <li class="stream-container"><img src=${feed} width="640" height="480" /></li>
        `
    });

    cameraList.innerHTML = newInnerHTML;
}
