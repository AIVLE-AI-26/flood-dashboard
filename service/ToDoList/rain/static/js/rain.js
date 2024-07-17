document.addEventListener('DOMContentLoaded', function() {
    fetchRainfallData();
});

let modalChartInstance;

async function fetchRainfallData() {
    document.getElementById('loading').style.display = 'block';
    document.querySelector('.chart-wrapper').style.display = 'none';
    try {
        const response = await fetch(fetchRainfallDataUrl);
        const data = await response.json();
        
        // API 응답 데이터를 콘솔에 출력
        console.log('API Response Data:', data);

        renderAllCharts(data.all_data);
        document.getElementById('loading').style.display = 'none';
        document.querySelector('.chart-wrapper').style.display = 'block';
        showCurrentRainfall(data.current_data);
        // 저장 데이터를 전역 변수에 저장
        window.rainfallData = data.all_data;
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
        const temperatureData = filteredData.map(row => row.temperature); // 온도 데이터
        renderChart(labels, rainfallData, temperatureData, `rainfallChart${index + 1}`);
    });
}

function formatTime(time) {
    return time.slice(0, 2) + ':' + time.slice(2, 4);
}

function renderChart(labels, rainfallData, temperatureData, canvasId) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: '강수량 (mm)',
                    data: rainfallData,
                    fill: false,
                    borderColor: '#3b80c6',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.4,
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
                },
                {
                    label: '온도 (°C)', // 온도 데이터 추가
                    data: temperatureData,
                    fill: false,
                    borderColor: '#ff6347',
                    backgroundColor: 'rgba(255, 99, 71, 0.2)',
                    tension: 0.4,
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(255, 99, 71, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(255, 99, 71, 1)'
                }
            ]
        },
        options: {
            plugins: {
                legend: {
                    display: true
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleFont: {
                        size: 16,
                        family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif"
                    },
                    bodyFont: {
                        size: 14,
                        family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif"
                    },
                    footerFont: {
                        size: 12,
                        family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif"
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: false
                    },
                    ticks: {
                        color: '#666',
                        callback: function(value, index, values) {
                            return value % 3 === 0 ? value : '';
                        }
                    },
                    grid: {
                        display: true,
                        drawOnChartArea: false,
                        drawTicks: false,
                        color: 'rgba(200, 200, 200, 0.3)'
                    }
                },
                y: {
                    title: {
                        display: false
                    },
                    ticks: {
                        color: '#666'
                    },
                    grid: {
                        drawBorder: false,
                        drawOnChartArea: true,
                        drawTicks: false,
                        color: 'rgba(200, 200, 200, 0.3)'
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

function openModal(title, location) {
    document.getElementById('modal-title').innerText = title;
    var modal = document.getElementById("myModal");

    // 필터링된 데이터 가져오기
    const filteredData = window.rainfallData.filter(row => row.location === location);
    const labels = filteredData.map(row => formatTime(row.fcst_time));
    const rainfallData = filteredData.map(row => row.fcst_value);
    const temperatureData = filteredData.map(row => row.temperature); // 온도 데이터 추가

    // 모달 창이 열릴 때마다 캔버스를 초기화
    var modalChartCanvas = document.getElementById("modal-chart");
    var newCanvas = document.createElement("canvas");
    newCanvas.id = "modal-chart";
    modalChartCanvas.parentNode.replaceChild(newCanvas, modalChartCanvas);

    var modalChart = newCanvas.getContext('2d');
    modalChartInstance = new Chart(modalChart, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: '강수량 (mm)',
                    data: rainfallData,
                    fill: false,
                    borderColor: '#3b80c6',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.4,
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(75, 192, 192, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
                },
                {
                    label: '온도 (°C)', // 온도 데이터 추가
                    data: temperatureData,
                    fill: false,
                    borderColor: '#ff6347',
                    backgroundColor: 'rgba(255, 99, 71, 0.2)',
                    tension: 0.4,
                    borderWidth: 2,
                    pointBackgroundColor: 'rgba(255, 99, 71, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(255, 99, 71, 1)'
                }
            ]
        },
        options: {
            plugins: {
                legend: {
                    display: true
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleFont: {
                        size: 16,
                        family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif"
                    },
                    bodyFont: {
                        size: 14,
                        family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif"
                    },
                    footerFont: {
                        size: 12,
                        family: "'Helvetica Neue', 'Helvetica', 'Arial', sans-serif"
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: false
                    },
                    ticks: {
                        color: '#666'
                    },
                    grid: {
                        display: true,
                        drawOnChartArea: false,
                        drawTicks: false,
                        color: 'rgba(200, 200, 200, 0.3)'
                    }
                },
                y: {
                    title: {
                        display: false
                    },
                    ticks: {
                        color: '#666'
                    },
                    grid: {
                        drawBorder: false,
                        drawOnChartArea: true,
                        drawTicks: false,
                        color: 'rgba(200, 200, 200, 0.3)'
                    }
                }
            }
        }
    });

    modal.style.display = "flex";
}

function closeModal() {
    var modal = document.getElementById("myModal");
    modal.style.display = "none";
    if (modalChartInstance) {
        modalChartInstance.destroy();
        modalChartInstance = null;
    }   
}

document.addEventListener('DOMContentLoaded', function() {
    fetchRainfallData();
});
