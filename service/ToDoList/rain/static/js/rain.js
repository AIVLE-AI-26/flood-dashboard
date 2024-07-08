document.addEventListener('DOMContentLoaded', function() {
    fetchRainfallData();
});

async function fetchRainfallData() {
    document.getElementById('loading').style.display = 'block';
    document.querySelector('.chart-wrapper').style.display = 'none';
    try {
        const response = await fetch(fetchRainfallDataUrl);
        const data = await response.json();
        renderAllCharts(data.all_data);
        document.getElementById('loading').style.display = 'none';
        document.querySelector('.chart-wrapper').style.display = 'block';
        showCurrentRainfall(data.current_data);
    } catch (error) {
        console.log('Error:', error);
        document.getElementById('loading').style.display = 'none';
    }
}

function renderAllCharts(data) {
    const locations = ['광주광역시', '동구', '서구', '남구', '북구', '광산구'];
    locations.forEach((location, index) => {
        const filteredData = data.filter(row => row.location === location);
        const labels = filteredData.map(row => formatTime(row.fcst_time));
        const rainfallData = filteredData.map(row => row.fcst_value);
        renderChart(labels, rainfallData, `rainfallChart${index + 1}`);
    });
}

function formatTime(time) {
    return time.slice(0, 2);
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
                    },
                    ticks: {
                        callback: function(value, index, values) {
                            return value % 3 === 0 ? value : '';
                        }
                    },
                    grid: {
                        display: true,
                        drawOnChartArea: false,
                        drawTicks: false
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Rainfall (mm)'
                    },
                    grid: {
                        drawBorder: false,
                        drawOnChartArea: true,
                        drawTicks: false,
                    }
                }
            }
        }
    });
}

function showCurrentRainfall(currentData) {
    const locations = ['광주광역시', '동구', '서구', '남구', '북구', '광산구'];
    locations.forEach(location => {
        const currentRainfallElement = document.getElementById(`current-rainfall-${location}`);
        if (currentData[location].length > 0) {
            currentRainfallElement.innerHTML = `현재 강수량: ${currentData[location][0].fcst_value} mm`;
        } else {
            currentRainfallElement.innerHTML = `${location} 데이터 없음.`;
        }
    });
}