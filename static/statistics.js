import { createClient } from "https://esm.sh/@supabase/supabase-js";

// Initialize the Supabase client
const SUPABASE_URL = "https://vpofkrbxyaxvzryhmdte.supabase.co";
const SUPABASE_ANON_KEY = "sb_publishable_T_AjtavafPYU-ciQ4q_Lfg_t08Xv47P"; // Safe for browser

const  client= createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const tomatoLeafClasses = [
    'Early Blight',
    'Healthy',
    'Late Blight',
    'Leaf Miner',
    'Leaf Mold',
    'Mosaic Virus',
    'Septoria',
    'Spider Mites',
    'Yellow Leaf Curl Virus'
]

const barColours = [
    "#b91d47", // Dark Red
    "#00aba9", // Teal
    "#2b5797", // Dark Blue
    "#e8c3b9", // Light Pink/Sandy
    "#1e7145", // Dark Green
    "#ff9f40", // Orange
    "#ffcd56", // Yellow
    "#4bc0c0", // Turquoise
    "#9966ff"  // Purple
];


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

    createLineChart(data);
    createPieChart(data);
    createBarChart(data);

}

function createLineChart(data) {
    const detectionChartCtx = new Chart("detectionChart", {
        type: 'line',
        data: {
            labels: data.map(item => new Date(item.created_at).toLocaleDateString()), // X-axis labels formatted (date only)
            datasets: [{
                label: 'Total Detections Over Time',
                data: data.filter(item => item.total_count >= 0).map(item => item.total_count), // Y-axis data is total_count
                borderColor: '#ff5722',
                backgroundColor: 'rgba(255, 87, 34, 0.1)',
                borderWidth: 2,
                tension: 0.2,
                fill: true
            }]
        },
        options: {
            maintainAspectRatio: false,
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

}

function createPieChart(data) {


    const detectionClassChartCtx = new Chart("detectionClassChart", {
        type: 'pie',
        data: {
            labels: tomatoLeafClasses,
            datasets: [{
                backgroundColor: barColours,
                data: tomatoLeafClasses.map((cls, index) => data.reduce((sum, item) => sum + (item[cls.toLowerCase().replace(/ /g, '_')] || 0), 0))
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: 'white',
                        font: {size:14}
                    }
                },
                title: {
                    display: true,
                    text: "Types of Detections",
                    font: {size:18},
                    color: "white"
                }
            }
        }
    });

    console.log(`[Chart] Created pie chart for detection classes: ${tomatoLeafClasses.map((cls, index) => `${cls}: ${data.reduce((sum, item) => sum + (item[cls.toLowerCase().replace(/ /g, '_')] || 0), 0)}`).join(', ')}`);
}

function createBarChart(data){
    const detectionClassBarChartCtx = new Chart("barChart", {
        type: 'bar',
        data: {
            labels: tomatoLeafClasses,
            datasets: [{
                backgroundColor: barColours,
                data: tomatoLeafClasses.map((cls, index) => data.reduce((sum, item) => sum + (item[cls.toLowerCase().replace(/ /g, '_')] || 0), 0))
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    })
}

// Call the function on page load
fetchStatistics();
