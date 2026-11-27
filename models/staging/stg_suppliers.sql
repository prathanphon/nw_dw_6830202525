{{ config(
    materialized='view',
    schema='staging'
) }}

SELECT *
FROM {{ source('northwind_raw', 'suppliers') }}
