from prophet import Prophet
import pandas as pd

def train_prophet(df: pd.DataFrame) -> Prophet:
    """
    Expects df with columns ['dt', 'temp'].
    Returns a fitted Prophet model on daily mean temperature.
    """
    df_train = df.rename(columns={"dt": "ds", "temp": "y"})
    m = Prophet(
        yearly_seasonality=True,
        daily_seasonality=False,
        weekly_seasonality=False,
        seasonality_mode="additive",
    )
    m.fit(df_train)
    return m
