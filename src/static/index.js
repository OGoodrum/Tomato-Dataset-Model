const cameraList = document.querySelector('.cameraList');

let cameraFeeds = ["https://tomatoevaluationsystem.ca/video_feed"];

function updateCameraFeeds() {
    let newInnerHTML = '';
    cameraFeeds.forEach((feed, index) => {
        newInnerHTML += `
        <li class="stream-container">
            <a href="${feed}" target="_blank">
                <img src=${feed} width="640" height="480" />
            </a>
        </li>
        `
    });

    cameraList.innerHTML = newInnerHTML;
}

updateCameraFeeds();