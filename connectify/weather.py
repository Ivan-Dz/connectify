"""
Simple OpenWeather wrapper for Connectify MVP.

Features:
- class-based API
- API key from constructor or environment variable
- timeout and basic error handling
- normalized return (dict) or raises ConnectifyError
"""
import os
import requests
from typing import Optional, Dict, Any

API_KEY_ENV = "CONNECTIFY_OPENWEATHER_API_KEY"
DEFAULT_TIMEOUT = 10  # seconds


class ConnectifyError(Exception):
    """Base exception for Connectify errors"""


class OpenWeather:
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self, api_key: Optional[str] = None, timeout: int = DEFAULT_TIMEOUT):
        """Initialize with an API key or read from env var.

        Args:
            api_key: OpenWeatherMap API key (optional if set via env var)
            timeout: request timeout in seconds
        """
        self.api_key = api_key or os.getenv(API_KEY_ENV)
        self.timeout = timeout
        if not self.api_key:
            raise ConnectifyError(
                f"OpenWeather API key not provided. Set env var {API_KEY_ENV} or pass api_key to constructor"
            )

    def _request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params = params.copy()
        params["appid"] = self.api_key
        try:
            resp = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
        except requests.RequestException as e:
            raise ConnectifyError(f"HTTP request failed: {e}")

        if resp.status_code != 200:
            # Try to parse JSON error
            try:
                data = resp.json()
                message = data.get("message") or str(data)
            except Exception:
                message = resp.text
            raise ConnectifyError(f"OpenWeather API error ({resp.status_code}): {message}")

        try:
            return resp.json()
        except ValueError:
            raise ConnectifyError("OpenWeather returned invalid JSON")

    def get_city_weather(self, city: str, units: str = "metric", lang: str = "en") -> Dict[str, Any]:
        """Get current weather for a city.

        Args:
            city: city name, e.g. "Algiers" or "London,uk"
            units: "metric", "imperial", or "standard"
            lang: language code for description

        Returns:
            Parsed JSON as Python dict
        """
        if not city:
            raise ConnectifyError("city parameter is required")

        params = {"q": city, "units": units, "lang": lang}
        return self._request(params)

    def get_by_coords(self, lat: float, lon: float, units: str = "metric", lang: str = "en") -> Dict[str, Any]:
        if lat is None or lon is None:
            raise ConnectifyError("lat and lon are required")
        params = {"lat": lat, "lon": lon, "units": units, "lang": lang}
        return self._request(params)
