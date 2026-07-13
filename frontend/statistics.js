import { createClient } from "https://esm.sh/@supabase/supabase-js";

// Initialize the Supabase client
const SUPABASE_URL = "https://vpofkrbxyaxvzryhmdte.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_T_AjtavafPYU-ciQ4q_Lfg_t08Xv47P"; // Safe for browser

const  client= createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

// Example: Fetch data from a table named 'products'
async function fetchNumberOfImages() {
    const { data, error } = await client
        .from('tomato_detections')
        .select('*');

    if (error) {
        console.error("Error fetching data:", error);
        document.getElementById('data-container').innerText = "Failed to load data.";
        return;
    }

    // Render data dynamically into HTML
    const statsContainer = document.getElementById('totalImages');
    console.log("Fetched data:", data);
    statsContainer.innerText = data.length; // Display total number of images processed
}

async function fetchDetectionsCount() {
    const { data, error } = await client
        .from('tomato_detections')
        .select('total_count', { count: 'exact' });

    if (error) {
        console.error("Error fetching detection count:", error);
        document.getElementById('detectionsCount').innerText = "Failed to load data.";
        return;
    }

    const statsContainer = document.getElementById('detectionsCount');
    console.log("Fetched detection count:", data[0].total_count);
    statsContainer.innerText = data[0].total_count;
}

// Call the function on page load
fetchNumberOfImages();
fetchDetectionsCount();
