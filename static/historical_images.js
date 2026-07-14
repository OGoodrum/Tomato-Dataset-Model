// Load Supabase JS client from CDN
import { createClient } from 'https://esm.sh/@supabase/supabase-js';


const imageArea = document.querySelector('.imageArea');


const SUPABASE_URL = "https://vpofkrbxyaxvzryhmdte.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_T_AjtavafPYU-ciQ4q_Lfg_t08Xv47P"; // Safe for browser

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

let images = [];

function updateImageArea() {
    let newInnerHTML = '';
    images.forEach((item) => {
        if (item.image_url) {
            const formattedTime = new Date(item.created_at).toLocaleString();
            newInnerHTML += `
            <li class="image-container">
                <img src="${item.image_url}" width="640" height="480" />
                <div class="timestamp">${formattedTime}</div>
            </li>
            `;
        }
    });

    imageArea.innerHTML = newInnerHTML;
}


async function loadImagesFromSupabase() {
    try {
        const { data, error } = await supabase
            .from('tomato_detections')
            .select('image_url, created_at')
            .order('created_at', { ascending: false }); // Show newest first

        if (error) throw error;

        if (data) {
            images = data;
            updateImageArea();
        }
    } catch (err) {
        console.error("Error loading images from Supabase:", err);
    }
}


loadImagesFromSupabase();