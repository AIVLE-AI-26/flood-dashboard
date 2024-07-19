async function fetchWeatherData() {
    const response = await fetch("/api/weather/");
    const data = await response.json();
    const weatherDataDiv = document.getElementById('weather-data');

    let temperatureHtml = '<div class="weather-section">';
    let precipitationHtml = '<div class="weather-section">';
    let skyHtml = '<div class="weather-section">';

    data.forEach(item => {
        if (item.category === 'T1H') {
            if (item.fcst_value >= 30) {
                temperatureHtml += `<span class="icon">🔥</span> ${item.fcst_value}°C `;
            } else if (item.fcst_value >= 25) {
                temperatureHtml += `<span class="icon">🌡️</span>  ${item.fcst_value}°C `;
            } else if (item.fcst_value >= 15) {
                temperatureHtml += `<span class="icon">🌬️</span>  ${item.fcst_value}°C `;
            } else if (item.fcst_value >= 0) {
                temperatureHtml += `<span class="icon">❄️</span>  ${item.fcst_value}°C `;
            } else {
                temperatureHtml += `<span class="icon">🧊</span>  ${item.fcst_value}°C `;
            }        
        } else if (item.category === 'RN1') {
            if (item.fcst_value == 0) {
                precipitationHtml += `<span class="icon">💧</span>0mm`;
            } else if (item.fcst_value > 0 && item.fcst_value <= 5) {
                precipitationHtml += `<span class="icon">🌦️</span> ${item.fcst_value}mm`;
            } else if (item.fcst_value > 5 && item.fcst_value <= 15) {
                precipitationHtml += `<span class="icon">🌧️</span> ${item.fcst_value}mm`;
            } else if (item.fcst_value > 15) {
                precipitationHtml += `<span class="icon">⛈️</span> ${item.fcst_value}mm`;
            }
        } else if (item.category === 'SKY') {
            if (item.fcst_value == 1) {
                skyHtml += `<span>날씨 ☀️</span>`;
            } else if (item.fcst_value == 3) {
                skyHtml += `<span>날씨 ⛅</span>`;
            } else if (item.fcst_value == 4) {
                skyHtml += `<span>날씨 ☁️</span>`;
            }
        }
    });

    temperatureHtml += '</div>';
    precipitationHtml += '</div>';
    skyHtml += '</div>';

    weatherDataDiv.innerHTML = `
        <div class="weather-row">${temperatureHtml}${precipitationHtml}${skyHtml}</div>
    `;
}

document.addEventListener('DOMContentLoaded', fetchWeatherData);
