const cameraList = document.querySelector('.cameraList');

const cameraFeeds = window.video_links || [];

function updateCameraFeeds() {
    let newInnerHTML = '';
    cameraFeeds.forEach((feed, index) => {
        newInnerHTML += `
        <li class="stream-container">
            <a href="${feed.video_feed_link}" target="_blank">
                <img src=${feed.video_feed_link} width="640" height="480" />
            </a>
        </li>
        `
    });

    cameraList.innerHTML = newInnerHTML;
}

updateCameraFeeds();