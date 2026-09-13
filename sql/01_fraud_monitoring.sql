-- Analysis 1: Merchant categories with high failure/reversal rates (Potential Fraud)
WITH transaction_metrics AS (
    SELECT 
        d.transaction_category,
        d.merchant_payee,
        COUNT(t.transaction_id) AS total_transactions,
        SUM(t.amount) AS total_volume,
        ROUND(AVG(t.amount), 2) AS avg_ticket_size,
        COUNT(CASE WHEN s.status_type IN ('Failed', 'Reversed') THEN 1 END) AS flagged_transactions
    FROM transactions t
    JOIN transaction_details d ON t.transaction_id = d.transaction_id
    JOIN transaction_status s ON t.transaction_id = s.transaction_id
    GROUP BY d.transaction_category, d.merchant_payee
)
SELECT 
    transaction_category,
    merchant_payee,
    total_transactions,
    flagged_transactions,
    ROUND((flagged_transactions::numeric / total_transactions) * 100, 2) AS failure_rate_pct,
    total_volume,
    avg_ticket_size
FROM transaction_metrics
WHERE total_transactions >= 10
ORDER BY failure_rate_pct DESC, total_volume DESC;

-- Analysis 2: Amount Outliers by Spending Profile
WITH profile_limits AS (
    SELECT 
        t.transaction_id,
        t.account_number,
        a.spending_profile,
        t.amount,
        t.date_time,
        t.transaction_type,
        CASE 
            WHEN a.spending_profile = 'Low' THEN 500
            WHEN a.spending_profile = 'Medium' THEN 6000
            WHEN a.spending_profile = 'High' THEN 50000
        END AS threshold_amount
    FROM transactions t
    JOIN accounts a ON t.account_number = a.account_number
)
SELECT 
    transaction_id,
    account_number,
    spending_profile,
    amount,
    threshold_amount,
    ROUND(amount - threshold_amount, 2) AS excess_amount,
    date_time,
    transaction_type
FROM profile_limits
WHERE amount > threshold_amount
ORDER BY excess_amount DESC;