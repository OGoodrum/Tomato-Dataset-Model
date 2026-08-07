

const notificationList = document.querySelector('.notification-list');

let notifications = window.notificationData || [];
console.log(notifications);

function updateNotifications() {
    let newInnerHTML = '';
    
    // Sort notifications so that the newest detections appear first
    notifications.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    notifications.forEach((notification, index) => {
        const formattedTime = new Date(notification.created_at).toLocaleString();
        
        // Collate anomalies/detections
        const anomalies = [];
        const diseaseFields = {
            'Early Blight': notification.early_blight,
            'Late Blight': notification.late_blight,
            'Leaf Miner': notification.leaf_miner,
            'Leaf Mold': notification.leaf_mold,
            'Mosaic Virus': notification.mosaic_virus,
            'Septoria': notification.septoria,
            'Spider Mites': notification.spider_mites,
            'Yellow Leaf Curl Virus': notification.yellow_leaf_curl_virus
        };
        
        for (const [name, count] of Object.entries(diseaseFields)) {
            if (count > 0) {
                anomalies.push(`${name} (${count})`);
            }
        }
        
        let statusHtml = '';
        if (anomalies.length > 0) {
            statusHtml = `<span class="anamoly">Anomalies: ${anomalies.join(', ')}</span>`;
        } else if (notification.healthy > 0) {
            statusHtml = `<span class="healthy">All Clear (Healthy Leaves: ${notification.healthy})</span>`;
        } else {
            statusHtml = `<span class="empty">No tomato leaves detected</span>`;
        }

        newInnerHTML += `
        <li class="notification-container">
            <div class="notification-text">
                <h3>Detection Event #${notification.id || index + 1}</h3>
                <p class="notification-time">Time: ${formattedTime}</p>
                <p class="notification-status">${statusHtml}</p>
                <p class="notification-total-count">Total Count: ${notification.total_count || 0}</p>
            </div>
            ${notification.image_url ? `
            <div class="notification-image"">
                <a href="${notification.image_url}" target="_blank">
                    <img src="${notification.image_url}" alt="Detection Image"/>
                </a>
            </div>
            ` : ''}
        </li>
        `;
    });

    if (newInnerHTML === '') {
        newInnerHTML = '<li class="notification-container" style="justify-content: center; opacity: 0.5;">No notifications yet.</li>';
    }

    notificationList.innerHTML = newInnerHTML;
}



updateNotifications();