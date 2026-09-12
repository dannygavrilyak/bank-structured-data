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