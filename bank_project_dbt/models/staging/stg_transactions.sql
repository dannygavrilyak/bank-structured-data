WITH
source AS (
    SELECT * FROM {{ source('bank_raw', 'transactions') }}
),
renamed AS (
    SELECT 
        transaction_id,
        account_number,
        transaction_type,
        amount,
        date_time::timestamp AS transaction_at,
        date_time::date as transaction_date_time
    FROM source
)

SELECT * FROM renamed