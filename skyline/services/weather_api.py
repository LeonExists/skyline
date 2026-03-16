"""Weather service using the Open-Meteo API (free, no API key required)."""

import httpx
from dataclasses import dataclass
from datetime import date


WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


@dataclass
class GeoLocation:
    name: str
    latitude: float
    longitude: float
    country: str


@dataclass
class DailyForecast:
    date: date
    temp_max: float
    temp_min: float
    weather_code: int

    @property
    def condition(self) -> str:
        return WMO_CODES.get(self.weather_code, "Unknown")


@dataclass
class CurrentWeather:
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    weather_code: int
    uv_index: float
    precipitation: float

    @property
    def condition(self) -> str:
        return WMO_CODES.get(self.weather_code, "Unknown")


@dataclass
class WeatherData:
    location: GeoLocation
    current: CurrentWeather
    daily: list[DailyForecast]
    hourly_temps: list[float]


async def geocode(city: str) -> GeoLocation:
    """Convert a city name to coordinates using Open-Meteo Geocoding API."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "language": "en"},
        )
        resp.raise_for_status()
        data = resp.json()

    if not data.get("results"):
        raise ValueError(f"Location '{city}' not found")

    result = data["results"][0]
    return GeoLocation(
        name=result["name"],
        latitude=result["latitude"],
        longitude=result["longitude"],
        country=result.get("country", ""),
    )


async def fetch_weather(location: GeoLocation) -> WeatherData:
    """Fetch current weather and 7-day forecast from Open-Meteo."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location.latitude,
                "longitude": location.longitude,
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,uv_index,precipitation",
                "daily": "temperature_2m_max,temperature_2m_min,weather_code",
                "hourly": "temperature_2m",
                "temperature_unit": "fahrenheit",
                "wind_speed_unit": "mph",
                "forecast_days": 7,
                "forecast_hours": 24,
            },
        )
        resp.raise_for_status()
        data = resp.json()

    current_data = data["current"]
    current = CurrentWeather(
        temperature=current_data["temperature_2m"],
        feels_like=current_data["apparent_temperature"],
        humidity=current_data["relative_humidity_2m"],
        wind_speed=current_data["wind_speed_10m"],
        weather_code=current_data["weather_code"],
        uv_index=current_data["uv_index"],
        precipitation=current_data["precipitation"],
    )

    daily_data = data["daily"]
    daily = [
        DailyForecast(
            date=date.fromisoformat(daily_data["time"][i]),
            temp_max=daily_data["temperature_2m_max"][i],
            temp_min=daily_data["temperature_2m_min"][i],
            weather_code=daily_data["weather_code"][i],
        )
        for i in range(len(daily_data["time"]))
    ]

    hourly_temps = [t for t in data["hourly"]["temperature_2m"] if t is not None]

    return WeatherData(
        location=location,
        current=current,
        daily=daily,
        hourly_temps=hourly_temps,
    )


async def get_weather(city: str) -> WeatherData:
    """Main entry point: geocode a city and fetch its weather."""
    location = await geocode(city)
    return await fetch_weather(location)
