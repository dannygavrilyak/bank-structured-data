-- Analysis 2: Velocity Checks — Rapid successive transactions per account (Card Testing / Fraud)
WITH ranked_transactions AS (
    SELECT 
        account_number,
        transaction_id,
        amount,
        transaction_type,
        date_time,
        LAG(date_time) OVER (
            PARTITION BY account_number 
            ORDER BY date_time
        ) AS prev_transaction_time
    FROM transactions
)
SELECT 
    account_number,
    transaction_id,
    amount,
    transaction_type,
    date_time,
    prev_transaction_time,
    ROUND(EXTRACT(EPOCH FROM (date_time - prev_transaction_time)) / 60, 2) AS minutes_since_last_tx
FROM ranked_transactions
WHERE prev_transaction_time IS NOT NULL
  AND EXTRACT(EPOCH FROM (date_time - prev_transaction_time)) <= 600
ORDER BY minutes_since_last_tx ASC;