"""
04_forecasting.py
Forecasts monthly sales for the next 3 months using Holt-Winters
Exponential Smoothing (robust, no extra dependencies beyond statsmodels).

To install: pip install statsmodels --break-system-packages
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.holtwinters import ExponentialSmoothing

OUT_DIR = Path("../outputs")
OUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv("../data/cleaned_transactions.csv", parse_dates=["invoice_date"])
df = df[~df["is_return"]]

monthly = (
    df.set_index("invoice_date")
    .resample("ME")["line_total"]
    .sum()
)

# Drop the last month if it's a partial month (common in raw retail exports)
monthly = monthly.iloc[:-1] if monthly.index[-1].day < 28 else monthly

# Fit Holt-Winters (additive trend + seasonal, 12-month seasonality if enough history)
seasonal_periods = 12 if len(monthly) >= 24 else None
model = ExponentialSmoothing(
    monthly,
    trend="add",
    seasonal="add" if seasonal_periods else None,
    seasonal_periods=seasonal_periods,
)
fit = model.fit()

forecast_periods = 3
forecast = fit.forecast(forecast_periods)

# Plot history + forecast
plt.figure(figsize=(11, 5))
plt.plot(monthly.index, monthly.values, label="Actual", marker="o")
plt.plot(forecast.index, forecast.values, label="Forecast", marker="o", linestyle="--", color="red")
plt.title("Monthly Sales Forecast (Next 3 Months)")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT_DIR / "sales_forecast.png", dpi=150)
plt.close()

print("=== FORECAST (next 3 months) ===")
print(forecast.round(2))

forecast.to_csv(OUT_DIR / "sales_forecast.csv", header=["forecast_revenue"])
print(f"\nSaved forecast chart and CSV to {OUT_DIR}/")
