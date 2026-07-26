# Retail Sales Performance & Customer Analytics Dashboard

## Problem Statement

Retail businesses generate large volumes of transactional data daily, but this data
is often scattered across systems and difficult to translate into timely, actionable
insight. Stakeholders — sales, marketing, and category managers — need clear visibility
into **what is selling, who is buying, and where growth or risk is emerging**, without
having to manually query raw transaction logs.

This project simulates a business-analyst engagement: given a raw retail transactions
dataset (100K+ records), the goal is to clean and structure the data, answer specific
business questions through SQL and Python analysis, forecast near-term sales, segment
customers by value, and present findings through an interactive Power BI dashboard —
mirroring the deliverables expected in a real BA/PM/Data Analyst role.

## Business Objectives

1. **Sales Performance** — Identify top/bottom performing products, categories, and
   regions; understand seasonality and monthly/quarterly revenue trends.
2. **Customer Analytics** — Segment customers by purchase behavior (RFM: Recency,
   Frequency, Monetary) to identify high-value, at-risk, and churned customers.
3. **Forecasting** — Project next-period sales using historical trends to support
   inventory and revenue planning.
4. **Actionable Reporting** — Package findings into a stakeholder-facing dashboard
   with clear KPIs, not just raw charts.

## Key Business Questions

- Which products/categories drive the most revenue and profit?
- Which countries/regions are growing vs. declining?
- What is the monthly revenue trend, and is there seasonality?
- Who are our top 10% customers by revenue (VIP segment)?
- Which customers haven't purchased recently and are at risk of churn?
- What is the expected sales trend for the next 1–3 months?
- What is the average order value and how does it vary by segment?

## Deliverables

| # | Deliverable | Tool |
|---|---|---|
| 1 | Cleaned, structured dataset | Python (pandas) |
| 2 | Business-question SQL queries | SQL |
| 3 | Exploratory Data Analysis (EDA) with visuals | Python |
| 4 | Customer segmentation (RFM analysis) | Python |
| 5 | Sales forecast (next 1–3 months) | Python (statsmodels/Prophet) |
| 6 | Interactive KPI dashboard | Power BI |
| 7 | One-page summary of insights & recommendations | Markdown/PDF |

## Success Criteria

- Dashboard loads cleanly and answers all key business questions above without
  needing to touch raw data.
- Forecast is directionally reasonable when validated against a hold-out period.
- Customer segments are clearly defined and actionable (e.g., "target this segment
  with a re-engagement campaign").

## Dataset Used

**Online Retail II** (Kaggle) — UK-based online retailer, Dec 2010–Dec 2011.
After cleaning: **534,130 transactions**, **4,372 unique customers**, **3,938 unique products**.

## Results

- **Total Net Revenue:** £9.75M (Gross Revenue: £10.64M, ~16% attributable to returns)
- **Sales Orders:** ~19,960 | **Average Order Value:** £533
- **Return Rate:** 16.12%
- **Customer Segmentation (RFM):** 933 VIP/Champions customers (avg. £6,690 spend)
  vs. 353 "Needs Attention" customers (avg. £226 spend) — roughly a 30x value gap
  between the top and bottom segments.
- **Forecast:** Next 3 months (Jan–Mar 2012) projected at £1.06M → £1.09M → £1.12M,
  using Holt-Winters exponential smoothing.
- **Top market:** United Kingdom (dominant), followed by Netherlands, Eire, and Germany.

## Data Quality Notes

During development, two notable data-quality issues were identified and resolved:
1. A day/month ambiguity in date parsing (via text round-tripping) silently misassigned
   a subset of transactions to the wrong month — fixed by extracting date parts
   directly as numeric values instead of parsing formatted text.
2. Return-rate and revenue calculations required care to distinguish gross vs. net
   figures once cancelled/returned orders (prefixed "C" in invoice numbers) were
   accounted for.

## Final Deliverable

A 3-page interactive Power BI dashboard:
1. **Executive Overview** — KPIs, monthly revenue trend, top products, revenue by country
2. **Customer Analytics** — RFM segment breakdown, average value by segment, top customers
3. **Trends & Forecast** — actual vs. forecasted revenue, revenue by day of week

Supported by a full SQL + Python analysis pipeline (see `sql/` and `python/` folders).
