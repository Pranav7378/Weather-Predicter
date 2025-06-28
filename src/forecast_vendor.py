from __future__ import annotations
import requests
import pandas as pd
import datetime as dt
import os
import urllib.parse
import streamlit as st


def get_vendor_forecast(city: str) -> pd.DataFrame:
    """
    Fetch 15-day forecast from Visual Crossing using explicit date range.
    Returns a DataFrame with columns ['dt', 'temp'].
    """
    key = st.secrets.get("VC_KEY") or os.getenv("VC_KEY")
    if not key:
        raise RuntimeError("VC_KEY not found in secrets or environment")

    # Format date range: today → today + 15
    today = dt.date.today()
    future = today + dt.timedelta(days=15)

    # Encode city name properly for URL
    location = urllib.parse.quote(city.strip())

    # Use explicit range-based URL
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{location}/{today}/{future}"
        f"?unitGroup=metric&include=days&key={key}&contentType=json"
    )

    headers = {"User-Agent": "WeatherApp (student project)"}
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    data = r.json()
    df = pd.DataFrame(data["days"])[["datetime", "temp"]]
    df = df.rename(columns={"datetime": "dt"})
    df["dt"] = pd.to_datetime(df["dt"])

    return df
