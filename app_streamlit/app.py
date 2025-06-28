# app_streamlit/app.py  ───────────────────────────────────────────
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import pickle, datetime as dt, os
import pandas as pd
import plotly.express as px
import streamlit as st
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.forecast_vendor import get_vendor_forecast

# ─── Streamlit page config ──────────────────────────────────────
st.set_page_config(
    page_title="India Weather Forecast",
    layout="wide",
    page_icon="📈"
)

# ─── Gradient background CSS ────────────────────────────────────
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg,#00172B 0%,#004B7A 50%,#0073A9 100%);
        background-attachment: fixed;
    }
    section[data-testid="stSidebar"] > div:first-child {
        backdrop-filter: blur(4px);
        background-color: rgba(0,0,0,0.35);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ─── Sidebar controls ───────────────────────────────────────────
with st.sidebar:
    st.header("Controls")
    city = st.selectbox(
        "Choose city (pre‑trained)",
        ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad"],
        index=0,
    )
    years_hist = 10  # all pickles are 10‑year history
    days_forecast = st.slider("Days to predict", 3, 365, 30)

# ─── Load pre‑trained model ─────────────────────────────────────
pkl_path = Path(f"models/prophet_{city.lower()}_{years_hist}.pkl")
if not pkl_path.exists():
    st.error(
        f"No pre‑trained model found for {city}. "
        "Train it in Colab and commit the .pkl first."
    )
    st.stop()


@st.cache_resource
def load_model(path: Path):
    with open(path, "rb") as f:
        return pickle.load(f)


model = load_model(pkl_path)

# ─── Generate forecast from loaded model ────────────────────────
future = model.make_future_dataframe(periods=days_forecast)
df_model = (
    model.predict(future)[["ds", "yhat"]]
    .rename(columns={"ds": "dt", "yhat": "temp"})
    .assign(source="Your Model")
)

# Keep only forecast dates (today onward) and limit to 15 for comparison
today = pd.to_datetime(dt.date.today())
df_model = df_model[df_model["dt"] >= today].head(15)

# ─── Vendor forecast (Visual Crossing) ──────────────────────────
try:
    df_vendor = get_vendor_forecast(city).assign(source="Visual Crossing")
    # Align on dates that exist in both
    df_compare = df_vendor.merge(
        df_model[["dt", "temp"]],
        on="dt",
        suffixes=("_vendor", "_model"),
    )
    # Compute error metrics if overlap exists
    if not df_compare.empty:
        mae = mean_absolute_error(
            df_compare["temp_vendor"], df_compare["temp_model"]
        )
        rmse = mean_squared_error(df_compare["temp_vendor"], df_compare["temp_model"]) ** 0.5

        st.markdown(f"📈 **MAE (Model vs Vendor):** `{mae:.2f} °C`")
        st.markdown(f"📉 **RMSE (Model vs Vendor):** `{rmse:.2f} °C`")
    else:
        st.info("No overlapping dates to compute MAE/RMSE.")

    df_plot = pd.concat([df_model, df_vendor], ignore_index=True)

except Exception as e:
    st.warning(f"Vendor forecast unavailable → {e}")
    df_plot = df_model

# ─── Plot comparison ────────────────────────────────────────────
st.subheader(f"{city} – Forecast Comparison")
fig = px.line(
    df_plot,
    x="dt",
    y="temp",
    color="source",
    markers=True,
)
fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Temperature (°C)",
    legend_title="Source",
)
st.plotly_chart(fig, use_container_width=True)

st.caption(
    "Training data: Meteostat • Model: Prophet • Vendor forecast: Visual Crossing"
)
