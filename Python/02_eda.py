"""
02_eda.py
Exploratory Data Analysis on cleaned retail transactions.
Produces charts answering the key business questions and saves them
to ../outputs/ for inclusion in the summary report / Power BI prep.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
OUT_DIR = Path("../outputs")
OUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv("../data/cleaned_transactions.csv", parse_dates=["invoice_date"])
df_sales = df[~df["is_return"]]  # exclude returns for revenue analysis

# ------------------------------------------------------------------
# 1. Monthly revenue trend
# ------------------------------------------------------------------
monthly = (
    df_sales.set_index("invoice_date")
    .resample("ME")["line_total"]
    .sum()
    .reset_index()
)
plt.figure(figsize=(10, 5))
plt.plot(monthly["invoice_date"], monthly["line_total"], marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUT_DIR / "monthly_revenue_trend.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 2. Top 10 products by revenue
# ------------------------------------------------------------------
top_products = (
    df_sales.groupby("description")["line_total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
plt.figure(figsize=(10, 6))
top_products.sort_values().plot(kind="barh")
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.tight_layout()
plt.savefig(OUT_DIR / "top_10_products.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 3. Revenue by country (top 10, excluding home country if it dominates)
# ------------------------------------------------------------------
top_countries = (
    df_sales.groupby("country")["line_total"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
plt.figure(figsize=(10, 6))
top_countries.sort_values().plot(kind="barh", color="teal")
plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.tight_layout()
plt.savefig(OUT_DIR / "top_10_countries.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 4. Order value distribution
# ------------------------------------------------------------------
order_value = df_sales.groupby("invoice_no")["line_total"].sum()
plt.figure(figsize=(8, 5))
sns.histplot(order_value[order_value < order_value.quantile(0.95)], bins=50)
plt.title("Distribution of Order Value (95th percentile trimmed)")
plt.xlabel("Order Value")
plt.tight_layout()
plt.savefig(OUT_DIR / "order_value_distribution.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# 5. Day-of-week sales pattern
# ------------------------------------------------------------------
df_sales["day_of_week"] = df_sales["invoice_date"].dt.day_name()
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
dow_revenue = df_sales.groupby("day_of_week")["line_total"].sum().reindex(dow_order)
plt.figure(figsize=(9, 5))
dow_revenue.plot(kind="bar", color="coral")
plt.title("Revenue by Day of Week")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(OUT_DIR / "revenue_by_day_of_week.png", dpi=150)
plt.close()

# ------------------------------------------------------------------
# Summary stats printout (for the write-up doc)
# ------------------------------------------------------------------
print("=== KEY METRICS ===")
print(f"Total Revenue: {df_sales['line_total'].sum():,.2f}")
print(f"Total Orders: {df_sales['invoice_no'].nunique():,}")
print(f"Total Customers: {df_sales['customer_id'].nunique():,}")
print(f"Average Order Value: {order_value.mean():,.2f}")
return_orders = df.loc[df["is_return"], "invoice_no"].nunique()
total_orders = df["invoice_no"].nunique()
print(f"Return Rate (by order count): {return_orders / total_orders:.2%}")
print(f"\nCharts saved to {OUT_DIR}/")
