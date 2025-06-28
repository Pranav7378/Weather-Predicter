# app_streamlit/app.py
# ────────────────────────────────────────────────────────────────
# Streamlit demo: Time‑series weather forecast for Indian cities
# • Historical data  →  Meteostat  (no key)
# • ML model         →  Prophet
# • Vendor forecast  →  Visual Crossing  (VC_KEY in secrets)
# • UI styling       →  Gradient background via CSS
# ────────────────────────────────────────────────────────────────

# ---- Python‑path patch so we can `import src.*` ----
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

# ---- External imports ----
import os, pickle, datetime as dt
import pandas as pd
import plotly.express as px
import streamlit as st

# ---- Internal modules ----
from src.data_loader import load_hist
from src.model import train_prophet
from src.forecast_vendor import get_vendor_forecast

# ════════════════════════  Streamlit Config  ════════════════════════
st.set_page_config(
    page_title="India City Weather Forecast",
    layout="wide",
    page_icon="📈",
)

# ---- 🎨  Background CSS  (swap for an image if you like) ----
st.markdown(
    """
    <style>
    /* Full‑page diagonal gradient */
    .stApp {
        background: linear-gradient(135deg,#00172B 0%,#004B7A 50%,#0073A9 100%);
        background-attachment: fixed;
    }
    /* Make sidebar slightly translucent */
    section[data-testid="stSidebar"] > div:first-child {
        backdrop-filter: blur(4px);
        background-color: rgba(0,0,0,0.35);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ════════════════════════  Sidebar Controls  ════════════════════════
with st.sidebar:
    st.header("Controls")
    city = st.selectbox(
        "City",
        ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"],
        index=0,
    )
    years_hist = st.slider("Historical years", 1, 20, 10)
    days_forecast = st.slider("Forecast horizon (days)", 3, 365, 30)
    retrain = st.checkbox("Force retrain", value=False)

# ════════════  City → Coordinates (hard‑coded, no OW API) ═══════════
CITY_COORDS = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bangalore": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
}
lat, lon = CITY_COORDS[city]

# ════════════  Model caching (memory + disk)  ═══════════
mdl_key = f"{city.lower()}_{years_hist}"
pkl_path = Path("models") / f"prophet_{mdl_key}.pkl"
model_cache = st.session_state.setdefault("models", {})
model = None

if not retrain:
    model = model_cache.get(mdl_key)
    if model is None and pkl_path.exists():
        with open(pkl_path, "rb") as f:
            model = pickle.load(f)
            model_cache[mdl_key] = model

# ════════════  Train model if not cached  ═══════════
if model is None:
    with st.spinner(f"Downloading {years_hist} y weather for {city}…"):
        end_date = dt.datetime.utcnow().date() - dt.timedelta(days=1)
        start_date = end_date - dt.timedelta(days=365 * years_hist)
        df_hist = load_hist(start_date, end_date, lat, lon)

    with st.spinner("Training Prophet…"):
        model = train_prophet(df_hist)

    # cache for later
    model_cache[mdl_key] = model
    pkl_path.parent.mkdir(exist_ok=True)
    with open(pkl_path, "wb") as f:
        pickle.dump(model, f)

# ════════════  Your model forecast  ═══════════
future = model.make_future_dataframe(periods=days_forecast)
df_model = (
    model.predict(future)[["ds", "yhat"]]
    .rename(columns={"ds": "dt", "yhat": "temp"})
    .assign(source="Your Model")
)

# ════════════  Visual Crossing forecast  ═══════════
try:
    df_vendor = get_vendor_forecast(city).assign(source="Visual Crossing")
    df_plot = pd.concat([df_model.tail(15), df_vendor], ignore_index=True)
except Exception as e:
    st.warning(f"Vendor forecast unavailable → {e}")
    df_plot = df_model.tail(15)

# ════════════  Plot comparison  ═══════════
st.subheader(f"{city} – Forecast comparison")
fig = px.line(
    df_plot,
    x="dt",
    y="temp",
    color="source",
    markers=True,
    title=None,
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Temperature (°C)",
    legend_title="Source",
)
st.plotly_chart(fig, use_container_width=True)

# ════════════  Footer  ═══════════
st.caption(
    "Training data: Meteostat • Model: Prophet • Vendor forecast: Visual Crossing"
)
