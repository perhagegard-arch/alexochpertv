export function renderWeatherCard(content) {
  const { location, current, forecast } = content;

  const forecastHTML = forecast.map(d => `
    <div class="forecast-day">
      <span class="forecast-name">${d.day}</span>
      <span class="forecast-icon">${d.icon}</span>
      <span class="forecast-temps">${d.min}° / ${d.max}°</span>
    </div>
  `).join("");

  return `
    <div class="weather-card">
      <p class="weather-location">${esc(location)}</p>
      <div class="weather-current">
        <span class="weather-icon">${current.icon}</span>
        <span class="weather-temp">${current.temp}°</span>
      </div>
      <p class="weather-desc">${esc(current.description)}</p>
      <p class="weather-wind">💨 ${current.wind_speed} m/s ${esc(current.wind_dir)}</p>
      <div class="weather-forecast">${forecastHTML}</div>
    </div>
  `;
}

function esc(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
