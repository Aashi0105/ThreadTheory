"""Weather tool module for ThreadTheory Multi-Agent Stylist.

Integrates with Open-Meteo Geocoding and Forecast APIs to fetch real-time
weather data without requiring an API key.
"""

import time
from typing import Dict, Any, Tuple
import requests


# WMO Weather interpretation codes mapping (Open-Meteo standard)
WMO_CODE_MAP = {
    0: "Clear Sky",
    1: "Mainly Clear",
    2: "Partly Cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing Rime Fog",
    51: "Light Drizzle",
    53: "Moderate Drizzle",
    55: "Dense Drizzle",
    61: "Slight Rain",
    63: "Moderate Rain",
    65: "Heavy Rain",
    71: "Slight Snow",
    73: "Moderate Snow",
    75: "Heavy Snow",
    80: "Slight Rain Showers",
    81: "Moderate Rain Showers",
    82: "Violent Rain Showers",
    95: "Thunderstorm",
    96: "Thunderstorm with Slight Hail",
    99: "Thunderstorm with Heavy Hail",
}

DEFAULT_HEADERS = {"User-Agent": "ThreadTheoryStylist/1.0 (Python/Requests)"}


def _fetch_with_retry(url: str, max_retries: int = 3, timeout: int = 15) -> requests.Response:
    """Helper function to execute HTTP GET with custom User-Agent, retries, and debug logging."""
    print(f"[DEBUG WeatherTool] Request URL: {url}")
    
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
            print(f"[DEBUG WeatherTool] HTTP Status Code: {response.status_code}")
            
            if response.status_code in (500, 502, 503, 504) and attempt < max_retries:
                print(f"[DEBUG WeatherTool] Received {response.status_code} (Service Unavailable). Retrying attempt {attempt}/{max_retries}...")
                time.sleep(1.0 * attempt)
                continue

            if not response.ok:
                print(f"[DEBUG WeatherTool] Request Failed! Status: {response.status_code}")
                print(f"[DEBUG WeatherTool] Response Body: {response.text[:300]}")

            response.raise_for_status()
            return response
        except requests.RequestException as e:
            last_error = e
            if attempt < max_retries:
                time.sleep(1.0 * attempt)
            else:
                raise e

    raise last_error or requests.RequestException(f"Failed request to {url}")


def geocode_city(city: str) -> Tuple[float, float, str]:
    """Converts a city name to latitude, longitude, and normalized city name using Open-Meteo Geocoding API.

    Args:
        city: Name of the city (e.g., "Vadodara", "London", "Tokyo").

    Returns:
        Tuple containing (latitude, longitude, normalized_city_name).

    Raises:
        ValueError: If the city cannot be resolved or found.
        requests.RequestException: If network connectivity or HTTP error occurs.
    """
    if not city or not city.strip():
        raise ValueError("City name cannot be empty.")

    cleaned_city = city.strip()
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={cleaned_city}&count=1&language=en&format=json"

    response = _fetch_with_retry(geocoding_url)

    data = response.json()
    results = data.get("results")

    if not results or len(results) == 0:
        raise ValueError(f"City '{cleaned_city}' could not be found. Please check spelling.")

    location = results[0]
    lat = float(location["latitude"])
    lon = float(location["longitude"])
    name = location.get("name", cleaned_city)

    return lat, lon, name


def get_weather(city: str) -> Dict[str, Any]:
    """Fetches real-time weather information for a given city via Open-Meteo.

    Args:
        city: Name of the city to look up.

    Returns:
        Dict containing structured weather data:
            - city: str
            - temperature: float (°C)
            - weather: str (human readable description)
            - rain_probability: int (%)
            - wind_speed: float (km/h)

    Raises:
        ValueError: If city name is invalid or not found.
        requests.RequestException: On API connection failure.
    """
    lat, lon, resolved_city_name = geocode_city(city)

    forecast_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,weather_code,wind_speed_10m"
        f"&daily=precipitation_probability_max"
        f"&timezone=auto"
    )

    response = _fetch_with_retry(forecast_url)

    data = response.json()

    # Extract current weather data
    current = data.get("current", {})
    temperature = round(float(current.get("temperature_2m", 0.0)), 1)
    weather_code = int(current.get("weather_code", 0))
    wind_speed = round(float(current.get("wind_speed_10m", 0.0)), 1)

    # Decode WMO weather condition code
    weather_description = WMO_CODE_MAP.get(weather_code, f"Code {weather_code}")

    # Extract max precipitation probability for today
    daily = data.get("daily", {})
    rain_probs = daily.get("precipitation_probability_max", [0])
    rain_probability = int(rain_probs[0]) if rain_probs else 0

    return {
        "city": resolved_city_name,
        "temperature": temperature,
        "weather": weather_description,
        "rain_probability": rain_probability,
        "wind_speed": wind_speed,
    }
