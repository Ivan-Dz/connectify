import os
from typing import Any, Dict, Optional

from .errors import ConnectifyError
from .http import get_json, AsyncHTTPClient

API_KEY_ENV = "CONNECTIFY_OPENWEATHER_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class _BaseWeather:
    def __init__(self, api_key: Optional[str] = None, timeout: int = 10):
        self.api_key = api_key or os.getenv(API_KEY_ENV)
        self.timeout = timeout
        if not self.api_key:
            raise ConnectifyError(f"OpenWeather API key not provided. Set env var {API_KEY_ENV} or pass api_key")

    @staticmethod
    def _normalize(data: Dict[str, Any]) -> Dict[str, Any]:
        weather = (data.get("weather") or [{}])[0]
        main = data.get("main", {})
        wind = data.get("wind", {})
        return {
            "city": data.get("name"),
            "country": data.get("sys", {}).get("country"),
            "temperature": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "temp_min": main.get("temp_min"),
            "temp_max": main.get("temp_max"),
            "pressure": main.get("pressure"),
            "humidity": main.get("humidity"),
            "description": weather.get("description"),
            "wind_speed": wind.get("speed"),
            "raw": data,
        }


class OpenWeather(_BaseWeather):
    """Sync OpenWeather client."""
    
    def _request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params = params.copy()
        params["appid"] = self.api_key
        return get_json(BASE_URL, params=params, timeout=self.timeout)

    def get_city_weather(self, city: str, units: str = "metric", lang: str = "en") -> Dict[str, Any]:
        if not city:
            raise ConnectifyError("city parameter is required")
        raw = self._request({"q": city, "units": units, "lang": lang})
        return self._normalize(raw)

    def get_by_coords(self, lat: float, lon: float, units: str = "metric", lang: str = "en") -> Dict[str, Any]:
        if lat is None or lon is None:
            raise ConnectifyError("lat and lon are required")
        raw = self._request({"lat": lat, "lon": lon, "units": units, "lang": lang})
        return self._normalize(raw)


class AsyncOpenWeather(_BaseWeather):
    """Async OpenWeather client."""
    
    def __init__(self, api_key: Optional[str] = None, timeout: int = 10, retries: int = 2):
        super().__init__(api_key=api_key, timeout=timeout)
        self.retries = retries
        self._client = None

    async def __aenter__(self):
        self._client = AsyncHTTPClient(timeout=self.timeout, retries=self.retries)
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._client:
            await self._client.__aexit__(exc_type, exc, tb)

    async def _request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        params = params.copy()
        params["appid"] = self.api_key
        return await self._client.get_json(BASE_URL, params=params)

    async def get_city_weather(self, city: str, units: str = "metric", lang: str = "en") -> Dict[str, Any]:
        if not city:
            raise ConnectifyError("city parameter is required")
        raw = await self._request({"q": city, "units": units, "lang": lang})
        return self._normalize(raw)

    async def get_by_coords(self, lat: float, lon: float, units: str = "metric", lang: str = "en") -> Dict[str, Any]:
        if lat is None or lon is None:
            raise ConnectifyError("lat and lon are required")
        raw = await self._request({"lat": lat, "lon": lon, "units": units, "lang": lang})
        return self._normalize(raw)