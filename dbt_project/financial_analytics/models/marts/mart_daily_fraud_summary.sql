{{config( materialized = 'table')}}

select 
    step_hour,
    transaction_type,
    count(*) as total_transactions,
    sum(amount) as total_amount,
    avg(amount) as average_amount,
    cast (sum(is_fraud) as INTEGER) as fraud_count,
    round(sum(is_fraud)*100.0 / count(*),2) as fraud_rate_pct
from {{ ref ('stg_transactions')}}
group by step_hour, transaction_type
order by step_hour, transaction_type