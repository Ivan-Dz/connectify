import argparse
import os
import sys
import asyncio

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from connectify import OpenWeather, AsyncOpenWeather, ConnectifyError


def _print_weather(data):
    city = data.get("city") or "Unknown"
    temp = data.get("temperature")
    desc = data.get("description") or ""
    country = data.get("country") or ""
    print(f"{city}, {country} — {temp}°C — {desc}")


def main():
    parser = argparse.ArgumentParser(prog="connectify", description="Connectify CLI (weather MVP)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    w = sub.add_parser("weather", help="Get weather for a city (sync)")
    w.add_argument("city", help="City name, e.g. Algiers")
    w.add_argument("--units", choices=["metric", "imperial", "standard"], default="metric")
    w.add_argument("--lang", default="en")
    w.add_argument("--apikey", default=None)

    aw = sub.add_parser("aweather", help="Get weather for a city (async)")
    aw.add_argument("city", help="City name, e.g. Algiers")
    aw.add_argument("--units", choices=["metric", "imperial", "standard"], default="metric")
    aw.add_argument("--lang", default="en")
    aw.add_argument("--apikey", default=None)

    args = parser.parse_args()

    if args.cmd == "weather":
        try:
            api_key = args.apikey or os.getenv("CONNECTIFY_OPENWEATHER_API_KEY")
            api = OpenWeather(api_key=api_key)
            data = api.get_city_weather(args.city, units=args.units, lang=args.lang)
            _print_weather(data)
        except ConnectifyError as e:
            print(f"[Error] {e}")
            sys.exit(1)
    elif args.cmd == "aweather":
        async def _run():
            try:
                api_key = args.apikey or os.getenv("CONNECTIFY_OPENWEATHER_API_KEY")
                async with AsyncOpenWeather(api_key=api_key) as client:
                    data = await client.get_city_weather(args.city, units=args.units, lang=args.lang)
                    _print_weather(data)
            except ConnectifyError as e:
                print(f"[Error] {e}")
                sys.exit(1)
        
        asyncio.run(_run())


if __name__ == "__main__":
    main()
