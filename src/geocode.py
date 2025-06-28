"""
Light wrapper around OpenWeatherMap Geocoding API.
Free tier: 1 000 calls / day.
"""

from __future__ import annotations
from functools   import lru_cache
from typing      import Tuple, Optional
import os, requests
from dotenv import load_dotenv

# Load variables from .env at import time
load_dotenv()                     # ensures OW_KEY is in os.environ

@lru_cache(maxsize=512)
def get_coordinates(
    city: str,
    state: str = "",
    country: str = "IN",
    api_key: str | None = None,
) -> Tuple[Optional[float], Optional[float]]:
    """
    Return (lat, lon) for a city name. Falls back to .env key automatically.
    """
    api_key = api_key or os.getenv("OW_KEY")
    if not api_key:
        raise ValueError(
            "❌ OpenWeatherMap API key not found. "
            "Add OW_KEY to your .env or pass api_key explicitly."
        )

    url = (
        "https://api.openweathermap.org/geo/1.0/direct"
        f"?q={city},{state},{country}&limit=1&appid={api_key}"
    )
    res = requests.get(url, timeout=10)
    res.raise_for_status()
    data = res.json()

    if not data:
        return None, None                    # city not found
    return data[0]["lat"], data[0]["lon"]
