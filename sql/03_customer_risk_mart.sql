-- Analysis 3: Customer Risk Profile Data Mart
DROP VIEW IF EXISTS v_customer_risk_profile;

CREATE VIEW v_customer_risk_profile AS
WITH customer_tx_stats AS (
    SELECT 
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS full_name,
        c.city,
        COUNT(t.transaction_id) AS total_transactions,
        COALESCE(SUM(t.amount), 0) AS total_spent,
        ROUND(COALESCE(AVG(t.amount), 0), 2) AS avg_transaction_amount,
        COUNT(CASE WHEN s.status_type IN ('Failed', 'Reversed') THEN 1 END) AS total_flagged_tx
    FROM customers c
    LEFT JOIN accounts a ON c.customer_id = a.customer_id
    LEFT JOIN transactions t ON a.account_number = t.account_number
    LEFT JOIN transaction_status s ON t.transaction_id = s.transaction_id
    GROUP BY c.customer_id, c.first_name, c.last_name, c.city
)
SELECT 
    customer_id,
    full_name,
    city,
    total_transactions,
    total_spent,
    avg_transaction_amount,
    total_flagged_tx,
    CASE 
        WHEN total_flagged_tx >= 3 OR (total_transactions > 0 AND (total_flagged_tx::numeric / total_transactions) >= 0.20) THEN 'HIGH RISK'
        WHEN total_flagged_tx BETWEEN 1 AND 2 THEN 'MEDIUM RISK'
        ELSE 'LOW RISK'
    END AS risk_category
FROM customer_tx_stats
ORDER BY total_flagged_tx DESC, total_spent DESC;