with risk_cte as (
        select
           customer_id,
            
            
        from {{ ref('customer') }}
    )


select *
from customer_data