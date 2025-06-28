"""
Historical daily weather loader using Meteostat (no API key, no card).
----------------------------------------------------------------------
• Meteostat covers 40+ years of global weather from airport and
  weather‑station archives.
• We fetch daily data, keep the date and mean temperature (°C).
• If `tavg` (mean) is missing we fall back to the average of `tmin` & `tmax`.
"""

from __future__ import annotations

import datetime as dt
from functools import lru_cache
from typing import Union

import pandas as pd
from meteostat import Point, Daily


@lru_cache(maxsize=128)
def load_hist(
    start: Union[dt.date, dt.datetime],
    end: Union[dt.date, dt.datetime],
    lat: float,
    lon: float,
) -> pd.DataFrame:
    """
    Return a DataFrame with columns ['dt', 'temp'] for the requested
    [start, end] date range (inclusive).

    Parameters
    ----------
    start, end : datetime.date or datetime.datetime
        Date range to fetch; will be coerced to datetime.datetime.
    lat, lon : float
        Geographic coordinates of the location.

    Raises
    ------
    ValueError
        If Meteostat returns an empty dataset for the coordinates/dates.
    """

    # ── 🔁 Ensure start & end are datetime.datetime ─────────────────
    if isinstance(start, dt.date) and not isinstance(start, dt.datetime):
        start = dt.datetime.combine(start, dt.time.min)
    if isinstance(end, dt.date) and not isinstance(end, dt.datetime):
        end = dt.datetime.combine(end, dt.time.min)

    # ── Fetch data from Meteostat ───────────────────────────────────
    loc = Point(lat, lon)
    df = Daily(loc, start, end).fetch()  # index = DatetimeIndex

    if df.empty:
        raise ValueError(
            f"Meteostat returned no data for ({lat:.2f},{lon:.2f}) "
            f"from {start.date()} to {end.date()}"
        )

    # ── Reformat & choose temperature column ───────────────────────
    df = df.reset_index().rename(columns={"time": "dt"})  # date → column
    df["temp"] = (
        df["tavg"]
        if "tavg" in df.columns and df["tavg"].notna().any()
        else df[["tmin", "tmax"]].mean(axis=1)
    )

    return df[["dt", "temp"]]
