-- ============================================================
-- Retail Sales Performance & Customer Analytics — Analysis Queries
-- ============================================================

-- 1. Monthly revenue trend
SELECT
    DATE_FORMAT(invoice_date, '%Y-%m') AS month,
    ROUND(SUM(line_total), 2) AS revenue,
    COUNT(DISTINCT invoice_no) AS orders
FROM transactions
WHERE quantity > 0
GROUP BY month
ORDER BY month;

-- 2. Top 10 products by revenue
SELECT
    stock_code,
    description,
    ROUND(SUM(line_total), 2) AS revenue,
    SUM(quantity) AS units_sold
FROM transactions
WHERE quantity > 0
GROUP BY stock_code, description
ORDER BY revenue DESC
LIMIT 10;

-- 3. Revenue by country (top 10)
SELECT
    country,
    ROUND(SUM(line_total), 2) AS revenue,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT invoice_no) AS orders
FROM transactions
WHERE quantity > 0
GROUP BY country
ORDER BY revenue DESC
LIMIT 10;

-- 4. Average order value (AOV) overall and by country
SELECT
    country,
    ROUND(SUM(line_total) / COUNT(DISTINCT invoice_no), 2) AS avg_order_value
FROM transactions
WHERE quantity > 0
GROUP BY country
ORDER BY avg_order_value DESC;

-- 5. RFM base query — Recency, Frequency, Monetary per customer
-- (run with a reference date = day after last transaction in dataset)
SELECT
    customer_id,
    DATEDIFF('2011-12-10', MAX(invoice_date)) AS recency_days,
    COUNT(DISTINCT invoice_no) AS frequency,
    ROUND(SUM(line_total), 2) AS monetary
FROM transactions
WHERE quantity > 0 AND customer_id IS NOT NULL
GROUP BY customer_id
ORDER BY monetary DESC;

-- 6. Top 10% customers by revenue (VIP segment) — window function approach
WITH customer_revenue AS (
    SELECT
        customer_id,
        SUM(line_total) AS revenue
    FROM transactions
    WHERE quantity > 0 AND customer_id IS NOT NULL
    GROUP BY customer_id
),
ranked AS (
    SELECT
        customer_id,
        revenue,
        PERCENT_RANK() OVER (ORDER BY revenue DESC) AS pct_rank
    FROM customer_revenue
)
SELECT customer_id, revenue
FROM ranked
WHERE pct_rank <= 0.10
ORDER BY revenue DESC;

-- 7. At-risk / churned customers — no purchase in last 90 days
SELECT
    customer_id,
    MAX(invoice_date) AS last_purchase,
    DATEDIFF(CURRENT_DATE, MAX(invoice_date)) AS days_since_last_purchase
FROM transactions
WHERE customer_id IS NOT NULL
GROUP BY customer_id
HAVING days_since_last_purchase > 90
ORDER BY days_since_last_purchase DESC;

-- 8. Returns / cancellations impact (invoice_no starting with 'C' in Online Retail II)
SELECT
    DATE_FORMAT(invoice_date, '%Y-%m') AS month,
    ROUND(SUM(line_total), 2) AS returned_value,
    COUNT(DISTINCT invoice_no) AS return_orders
FROM transactions
WHERE invoice_no LIKE 'C%'
GROUP BY month
ORDER BY month;
