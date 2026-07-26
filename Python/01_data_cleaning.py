"""
01_data_cleaning.py
Cleans the raw retail transactions dataset and outputs a clean CSV
ready for EDA, RFM segmentation, and forecasting.

Update CONFIG below to match your chosen Kaggle dataset's column names.
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ------------------------------------------------------------------
# CONFIG — remap these if your Kaggle dataset uses different column names
# ------------------------------------------------------------------
RAW_FILE = "../data/online_retail_II.csv"   # <-- point this at your downloaded file
OUTPUT_FILE = "../data/cleaned_transactions.csv"

COLUMN_MAP = {
    "Invoice": "invoice_no",
    "InvoiceNo": "invoice_no",
    "StockCode": "stock_code",
    "Description": "description",
    "Quantity": "quantity",
    "InvoiceDate": "invoice_date",
    "Price": "unit_price",
    "UnitPrice": "unit_price",
    "Customer ID": "customer_id",
    "CustomerID": "customer_id",
    "Country": "country",
}


def load_and_clean(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, encoding="ISO-8859-1")

    # Standardize column names
    df = df.rename(columns={c: COLUMN_MAP[c] for c in df.columns if c in COLUMN_MAP})

    # Parse dates
    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")

    # Drop rows with missing critical fields
    before = len(df)
    df = df.dropna(subset=["invoice_no", "stock_code", "invoice_date", "unit_price"])
    print(f"Dropped {before - len(df)} rows with missing critical fields")

    # Remove rows with non-positive price (data errors) — keep negative quantity
    # (negative quantity = returns, which we want for return-rate analysis)
    df = df[df["unit_price"] > 0]

    # Flag cancellations/returns (Online Retail II prefixes cancelled invoices with 'C')
    df["is_return"] = df["invoice_no"].astype(str).str.startswith("C")

    # Compute line total
    df["line_total"] = df["quantity"] * df["unit_price"]

    # Fill missing customer_id with a placeholder for guest checkouts
    df["customer_id"] = df["customer_id"].fillna("GUEST").astype(str)

    # Drop exact duplicates
    dup_count = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"Dropped {dup_count} duplicate rows")

    # Basic sanity report
    print(f"Final row count: {len(df):,}")
    print(f"Date range: {df['invoice_date'].min()} to {df['invoice_date'].max()}")
    print(f"Unique customers: {df['customer_id'].nunique():,}")
    print(f"Unique products: {df['stock_code'].nunique():,}")

    return df


if __name__ == "__main__":
    Path("../data").mkdir(exist_ok=True)
    df = load_and_clean(RAW_FILE)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSaved cleaned data to {OUTPUT_FILE}")
