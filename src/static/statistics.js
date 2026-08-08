

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

    let data = window.statisticsData || [];
    
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
    // Filter and normalize dates to local midnight to avoid time-of-day offsets
    const parsedItems = data
        .filter(item => item.total_count >= 0 && item.created_at)
        .map(item => {
            const d = new Date(item.created_at);
            return {
                date: new Date(d.getFullYear(), d.getMonth(), d.getDate()),
                count: item.total_count
            };
        });

    if (parsedItems.length === 0) {
        return;
    }

    // Sum counts by local date string
    const grouped = {};
    parsedItems.forEach(item => {
        const key = item.date.toLocaleDateString();
        grouped[key] = (grouped[key] || 0) + item.count;
    });

    // Find min date in milliseconds and use now as the max date
    const timeValues = parsedItems.map(item => item.date.getTime());
    const minTime = Math.min(...timeValues);
    const maxTime = Date.now();

    const labels = [];
    const chartData = [];

    // Fill in every day sequentially from min to max date
    let current = new Date(minTime);
    const end = new Date(maxTime);

    while (current <= end) {
        const key = current.toLocaleDateString();
        labels.push(key);
        chartData.push(grouped[key] || 0);

        // Advance by 1 day
        current.setDate(current.getDate() + 1);
    }

    const detectionChartCtx = new Chart("detectionChart", {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Total Detections Over Time',
                data: chartData,
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
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
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
