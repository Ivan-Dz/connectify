"""Basic tests for OpenWeather wrapper.

These are simple smoke tests. To run locally, set the environment variable
CONNECTIFY_OPENWEATHER_API_KEY to a valid key or pass a key in the test.
"""
import os
import pytest
from connectify.weather import OpenWeather, ConnectifyError

API_KEY = os.getenv("CONNECTIFY_OPENWEATHER_API_KEY")


def test_missing_api_key():
    # Temporarily ensure env var not set
    orig = os.environ.pop("CONNECTIFY_OPENWEATHER_API_KEY", None)
    try:
        with pytest.raises(ConnectifyError):
            OpenWeather()
    finally:
        if orig is not None:
            os.environ["CONNECTIFY_OPENWEATHER_API_KEY"] = orig


@pytest.mark.skipif(not API_KEY, reason="No OpenWeather API key provided in env")
def test_get_city_weather():
    ow = OpenWeather(api_key=API_KEY)
    res = ow.get_city_weather("Algiers")
    assert isinstance(res, dict)
    assert "weather" in res
