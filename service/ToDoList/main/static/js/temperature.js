async function fetchWeatherData() {
    const response = await fetch("/api/weather/");
    const data = await response.json();
    const weatherDataDiv = document.getElementById('weather-data');
    
    let html = '';
    data.forEach(item => {
        if (item.category === 'T1H') {
            html += `<p>현재 기온: ${item.fcst_value} °C</p>`;
        } else if (item.category === 'RN1') {
            html += `<p>현재 강수량: ${item.fcst_value} mm</p>`;
        }
    });
    
    weatherDataDiv.innerHTML = html;
}

document.addEventListener('DOMContentLoaded', fetchWeatherData);