WITH 
transactions AS (
    SELECT * FROM {{ ref('stg_transactions') }}
),
accounts AS (
    SELECT * FROM {{ ref('stg_accounts') }}
),
customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),
joined AS (
    SELECT t.transaction_id,
        t.transaction_type,
        t.amount,
        t.transaction_at,
        t.transaction_date_time,
        c.customer_id,
        c.full_name,
        a.account_number,
        a.account_type

    FROM transactions t
    LEFT JOIN accounts a
        ON t.account_number = a.account_number
    LEFT JOIN customers c
        ON a.customer_id = c.customer_id
)   

SELECT * FROM joined