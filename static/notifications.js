
import { createClient } from "https://esm.sh/@supabase/supabase-js";

// Initialize the Supabase client
const SUPABASE_URL = "https://vpofkrbxyaxvzryhmdte.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_T_AjtavafPYU-ciQ4q_Lfg_t08Xv47P"; // Safe for browser

const client = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const notificationList = document.querySelector('.notification-list');

let notifications = [];

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
            statusHtml = `<span style="color: #ff5722; font-weight: bold;">Anomalies: ${anomalies.join(', ')}</span>`;
        } else if (notification.healthy > 0) {
            statusHtml = `<span style="color: #4bc0c0;">All Clear (Healthy Leaves: ${notification.healthy})</span>`;
        } else {
            statusHtml = `<span style="opacity: 0.6;">No tomato leaves detected</span>`;
        }

        newInnerHTML += `
        <li class="notification-container" style="text-align: left; display: flex; justify-content: space-between; align-items: center; width: 100%; box-sizing: border-box; max-width: 800px; margin: 15px auto;">
            <div style="flex: 1; min-width: 0; padding-right: 15px;">
                <h3 style="margin: 0 0 5px 0; color: #ff5722; font-family: 'JetBrains Mono', monospace; font-size: 18px;">Detection Event #${notification.id || index + 1}</h3>
                <p style="margin: 0 0 8px 0; font-size: 13px; opacity: 0.7;">Time: ${formattedTime}</p>
                <p style="margin: 0 0 5px 0; font-size: 15px;">${statusHtml}</p>
                <p style="margin: 0; font-size: 14px; opacity: 0.9;">Total Count: ${notification.total_count || 0}</p>
            </div>
            ${notification.image_url ? `
            <div style="flex-shrink: 0;">
                <a href="${notification.image_url}" target="_blank">
                    <img src="${notification.image_url}" alt="Detection Image" style="border-radius: 6px; max-height: 80px; max-width: 120px; border: 2px solid #ff5722; display: block; object-fit: cover;" />
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

async function fetchTomatoDetections() {
    const { data, error } = await client
        .from('tomato_detections')
        .select('*');

    if (error) {
        console.error("Error fetching detection count:", error);
        return;
    }

    notifications = data || [];
    updateNotifications();
}

fetchTomatoDetections();