"""
Connectify — lightweight toolkit for common web APIs (MVP: OpenWeather).
"""
from .weather import OpenWeather, AsyncOpenWeather
from .errors import ConnectifyError

__all__ = ["OpenWeather", "AsyncOpenWeather", "ConnectifyError"]
__version__ = "0.1.1"