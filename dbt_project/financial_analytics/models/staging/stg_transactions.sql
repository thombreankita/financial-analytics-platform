{{config(materialized = 'view')}}

select 
    cast(step as int) as step_hour,
    cast(type as varchar) as transaction_type,
    cast(amount as double) as amount,
    cast(nameOrig as varchar) as sender_id,
    cast(oldbalanceOrg as double) as sender_balance_before,
    cast(newbalanceOrig as double) as sender_balance_after,
    cast(nameDest as varchar) as receiver_id,
    cast(oldbalanceDest as double) as receiver_balance_before,
    cast(newbalanceDest as double) as receiver_balance_after,
    cast(isFraud as int) as is_fraud,
    cast(isFlaggedFraud as int) as is_flagged_fraud
from {{ source('raw', 'paysim_raw') }}
where amount IS NOT NULL AND amount > 0