
import { createClient } from "https://esm.sh/@supabase/supabase-js";

// Initialize the Supabase client
const SUPABASE_URL = "https://vpofkrbxyaxvzryhmdte.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_T_AjtavafPYU-ciQ4q_Lfg_t08Xv47P"; // Safe for browser

const  client = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);


const notificationList  = document.querySelector('.notification-list');

let notifications = []

function updateNotifications(){
    let newInnerHTML = '';
    notifications.forEach((notification, index) => {
        newInnerHTML += `
        <li class="notification-container"></li>
        `
    });

    notificationList.innerHTML = newInnerHTML;
}

async function fetchTomatoDetections(){
    const { data, error } = await client
        .from('tomato_detections')
        .select('*');

    if (error) {
        console.error("Error fetching detection count:", error);
        return;
    }

    notifications = data;
}

await fetchTomatoDetections();
updateNotifications();