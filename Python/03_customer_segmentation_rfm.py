"""
03_customer_segmentation_rfm.py
Segments customers using RFM (Recency, Frequency, Monetary) analysis
and assigns each customer to a business-friendly segment.
"""

import pandas as pd
from pathlib import Path

OUT_DIR = Path("../outputs")
OUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv("../data/cleaned_transactions.csv", parse_dates=["invoice_date"])
df = df[(~df["is_return"]) & (df["customer_id"] != "GUEST")]

# Reference date = one day after the last transaction in the dataset
reference_date = df["invoice_date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("customer_id").agg(
    recency=("invoice_date", lambda x: (reference_date - x.max()).days),
    frequency=("invoice_no", "nunique"),
    monetary=("line_total", "sum"),
).reset_index()

# Score each dimension 1–5 using quintiles (5 = best)
rfm["r_score"] = pd.qcut(rfm["recency"], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm["m_score"] = pd.qcut(rfm["monetary"], 5, labels=[1, 2, 3, 4, 5]).astype(int)

rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]


def segment(row):
    if row["rfm_score"] >= 13:
        return "VIP / Champions"
    elif row["rfm_score"] >= 10:
        return "Loyal Customers"
    elif row["rfm_score"] >= 7:
        return "Potential Loyalists"
    elif row["r_score"] <= 2 and row["f_score"] <= 2:
        return "At Risk / Churned"
    else:
        return "Needs Attention"


rfm["segment"] = rfm.apply(segment, axis=1)

print("=== CUSTOMER SEGMENTS ===")
print(rfm["segment"].value_counts())
print("\n=== SEGMENT VALUE (avg monetary) ===")
print(rfm.groupby("segment")["monetary"].mean().sort_values(ascending=False).round(2))

rfm.to_csv(OUT_DIR / "customer_rfm_segments.csv", index=False)
print(f"\nSaved RFM segments to {OUT_DIR}/customer_rfm_segments.csv")
