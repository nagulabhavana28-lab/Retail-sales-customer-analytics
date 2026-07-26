-- ============================================================
-- Retail Sales Performance & Customer Analytics — Schema
-- Target: Online Retail II style dataset (remap if using another)
-- ============================================================

CREATE TABLE transactions (
    invoice_no      VARCHAR(20),
    stock_code      VARCHAR(20),
    description     VARCHAR(255),
    quantity        INT,
    invoice_date    DATETIME,
    unit_price      DECIMAL(10,2),
    customer_id     VARCHAR(20),
    country         VARCHAR(100)
);

-- Derived column used throughout analysis: line_total = quantity * unit_price
-- (computed in Python during cleaning and re-loaded, or via a generated column:)
ALTER TABLE transactions
    ADD COLUMN line_total DECIMAL(12,2)
    GENERATED ALWAYS AS (quantity * unit_price) STORED;

-- Indexes to speed up the analysis queries
CREATE INDEX idx_invoice_date ON transactions(invoice_date);
CREATE INDEX idx_customer_id  ON transactions(customer_id);
CREATE INDEX idx_country      ON transactions(country);
CREATE INDEX idx_stock_code   ON transactions(stock_code);
