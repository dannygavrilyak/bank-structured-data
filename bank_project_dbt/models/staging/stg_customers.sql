WITH
source AS (
    SELECT * FROM {{ source('bank_raw', 'customers')}}
),
renamed AS (
    SELECT customer_id,
        branch_id,
        first_name || ' ' || last_name as full_name,
        gender,
        date_of_birth::date as date_of_birth,
        city, state, country,
        email, phone,
        ssn
    FROM source
)

SELECT * FROM renamed