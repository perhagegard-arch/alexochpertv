import requests
from datetime import datetime, timezone, timedelta

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude={lat}&longitude={lon}"
    "&current=temperature_2m,wind_speed_10m,wind_direction_10m,weather_code"
    "&daily=weather_code,temperature_2m_max,temperature_2m_min"
    "&timezone=Europe/Stockholm&forecast_days=4"
)

WMO = {
    0:  ("Klart",              "☀️"),
    1:  ("Nästan klart",       "🌤️"),
    2:  ("Delvis molnigt",     "⛅"),
    3:  ("Mulet",              "☁️"),
    45: ("Dimma",              "🌫️"),
    48: ("Rimfrostdimma",      "🌫️"),
    51: ("Lätt duggregn",      "🌦️"),
    53: ("Duggregn",           "🌦️"),
    55: ("Tätt duggregn",      "🌧️"),
    61: ("Lätt regn",          "🌦️"),
    63: ("Regn",               "🌧️"),
    65: ("Kraftigt regn",      "🌧️"),
    71: ("Lätt snöfall",       "❄️"),
    73: ("Snöfall",            "❄️"),
    75: ("Kraftigt snöfall",   "❄️"),
    77: ("Snöflingor",         "❄️"),
    80: ("Lätt regnskur",      "🌦️"),
    81: ("Regnskur",           "🌧️"),
    82: ("Kraftig regnskur",   "🌧️"),
    85: ("Snöbyar",            "🌨️"),
    86: ("Kraftiga snöbyar",   "🌨️"),
    95: ("Åska",               "⛈️"),
    96: ("Åska med hagel",     "⛈️"),
    99: ("Kraftig åska",       "⛈️"),
}

SWEDISH_DAYS = ["Mån", "Tis", "Ons", "Tor", "Fre", "Lör", "Sön"]
WIND_DIRS = ["N","NNO","NO","ONO","O","OSO","SO","SSO","S","SSV","SV","VSV","V","VNV","NV","NNV"]


def _wind_dir(degrees):
    return WIND_DIRS[round(degrees / 22.5) % 16]


class WeatherProvider:
    def __init__(self, lat=58.4108, lon=15.6214, location="Linköping"):
        self.lat = lat
        self.lon = lon
        self.location = location
        self._cache = None
        self._cache_until = datetime.min.replace(tzinfo=timezone.utc)

    def get(self):
        now = datetime.now(timezone.utc)
        if self._cache and now < self._cache_until:
            return self._cache

        url = OPEN_METEO_URL.format(lat=self.lat, lon=self.lon)
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        result = self._parse(resp.json())

        self._cache = result
        self._cache_until = now + timedelta(minutes=10)
        return result

    def _parse(self, data):
        c = data["current"]
        code = c["weather_code"]
        desc, icon = WMO.get(code, ("", "❓"))

        current = {
            "temp": round(c["temperature_2m"]),
            "wind_speed": round(c["wind_speed_10m"] / 3.6, 1),  # km/h → m/s
            "wind_dir": _wind_dir(c["wind_direction_10m"]),
            "description": desc,
            "icon": icon,
        }

        today = datetime.now(timezone.utc).date().isoformat()
        forecast = []
        daily = data["daily"]
        for i, date_str in enumerate(daily["time"]):
            if date_str == today:
                continue
            if len(forecast) >= 3:
                break
            code = daily["weather_code"][i]
            _, f_icon = WMO.get(code, ("", "❓"))
            d = datetime.fromisoformat(date_str).date()
            forecast.append({
                "day": SWEDISH_DAYS[d.weekday()],
                "min": round(daily["temperature_2m_min"][i]),
                "max": round(daily["temperature_2m_max"][i]),
                "icon": f_icon,
            })

        return {
            "location": self.location,
            "current": current,
            "forecast": forecast,
        }
