import { createClient } from "https://esm.sh/@supabase/supabase-js";

// Initialize the Supabase client
const SUPABASE_URL = "https://vpofkrbxyaxvzryhmdte.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_T_AjtavafPYU-ciQ4q_Lfg_t08Xv47P"; // Safe for browser

const  client= createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
const detectionChartCtx = new Chart("detectionChart", {
    type: 'line',
    data: {
        labels: [], // X-axis labels (e.g., timestamps)
        datasets: [{
            backgroundColor: '#ff5722',
            label: 'Detections Over Time',
            data: [], // Y-axis data (e.g., detection counts)
        }],
    options: {}
    }
});

async function fetchStatistics() {

    const { data, error } = await client
        .from('tomato_detections')
        .select('*');

    if (error) {
        console.error("Error fetching detection count:", error);
        document.getElementById('detectionsCount').innerText = "Failed to load data.";
        return;
    }
    
    const totalImagesContainer = document.getElementById('totalImages');
    const detectionsCountContainer = document.getElementById('detectionsCount');

    console.log("Fetched data:", data);

    totalImagesContainer.innerText = data.length;
    detectionsCountContainer.innerText = data.reduce((sum, item) => sum + item.total_count, 0);
}

// Call the function on page load
fetchStatistics();
