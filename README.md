# Connectify — MVP (OpenWeather)

Minimal MVP for Connectify. This release provides a small, safe wrapper around **OpenWeatherMap** current weather API.

## Features
- `OpenWeather` class with `get_city_weather` and `get_by_coords` methods
- Basic error handling via `ConnectifyError`
- API key via env var `CONNECTIFY_OPENWEATHER_API_KEY` or constructor parameter

## Quickstart

```bash
pip install -r requirements.txt
export CONNECTIFY_OPENWEATHER_API_KEY=your_key_here
python -c "from connectify import OpenWeather; print(OpenWeather().get_city_weather('Algiers'))"
