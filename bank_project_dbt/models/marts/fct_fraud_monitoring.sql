WITH 
source AS (
    SELECT * FROM {{ ref('fct_customer_transactions') }}
),
finish AS (
    SELECT
        customer_id, full_name,
        COUNT(transaction_id) AS count_of_transactions,
        SUM(amount) AS total_amount_of_tx,
        ROUND(AVG(amount), 2) AS average_amount_of_tx,
        COUNT(CASE WHEN amount > 5000 THEN 1 END) AS high_amount_tx,
        CASE 
            WHEN SUM(amount) > 50000 OR COUNT(CASE WHEN amount > 5000 THEN 1 END) > 0 THEN 'HIGH RISK'
            ELSE 'STANDARD'
        END AS risk_category
    FROM source
    GROUP BY customer_id, full_name
    
)

SELECT * FROM finish
ORDER BY
    CASE WHEN risk_category = 'HIGH RISK' THEN 0 ELSE 1 END,
    total_amount_of_tx DESC