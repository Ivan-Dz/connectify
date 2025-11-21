import os
from unittest.mock import patch
import pytest

from connectify.weather import OpenWeather
from connectify.errors import ConnectifyError

SAMPLE_RESPONSE = {
    "name": "Algiers",
    "sys": {"country": "DZ"},
    "weather": [{"description": "clear sky"}],
    "main": {"temp": 25, "feels_like": 24, "humidity": 30, "pressure": 1012},
    "wind": {"speed": 3.4},
}


@patch("connectify.weather.get_json")
def test_get_city_weather(mock_get_json):
    mock_get_json.return_value = SAMPLE_RESPONSE
    os.environ["CONNECTIFY_OPENWEATHER_API_KEY"] = "testkey"
    api = OpenWeather()
    res = api.get_city_weather("Algiers")
    assert res["city"] == "Algiers"
    assert res["country"] == "DZ"
    assert res["temperature"] == 25
    assert res["description"] == "clear sky"


def test_missing_key():
    if "CONNECTIFY_OPENWEATHER_API_KEY" in os.environ:
        del os.environ["CONNECTIFY_OPENWEATHER_API_KEY"]
    with pytest.raises(ConnectifyError):
        OpenWeather()


@patch("connectify.weather.get_json")
def test_empty_city(mock_get_json):
    os.environ["CONNECTIFY_OPENWEATHER_API_KEY"] = "testkey"
    api = OpenWeather()
    with pytest.raises(ConnectifyError):
        api.get_city_weather("")