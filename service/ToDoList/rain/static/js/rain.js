document.addEventListener('DOMContentLoaded', function() {
    fetchRainfallData();
});

function fetchRainfallData() {
    $.ajax({
        url: fetchRainfallDataUrl,
        method: 'GET',
        success: function(data) {
            renderAllCharts(data);
        },
        error: function(error) {
            console.log('Error:', error);
        }
    });
}

function renderAllCharts(data) {
    const locations = ['광주광역시', '동구', '서구', '남구', '북구', '광산구'];
    locations.forEach((location, index) => {
        const filteredData = data.filter(row => row.location === location);
        const labels = filteredData.map(row => row.fcst_time);
        const rainfallData = filteredData.map(row => row.fcst_value);
        renderChart(labels, rainfallData, `rainfallChart${index + 1}`);
    });
}

function renderChart(labels, data, canvasId) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Rainfall (mm)',
                data: data,
                fill: false,
                borderColor: 'blue'
            }]
        },
        options: {
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Forecast Time'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Rainfall (mm)'
                    }
                }
            }
        }
    });
}