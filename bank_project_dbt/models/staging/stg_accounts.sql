WITH
source AS (
    SELECT * FROM {{ source('bank_raw', 'accounts')}}
),
renamed AS (
    SELECT account_number,
        customer_id,
        account_type,
        balance,
        account_status,
        registration_date,
        open_date,
        closed_date,
        spending_profile
    FROM source
)

SELECT * FROM renamed