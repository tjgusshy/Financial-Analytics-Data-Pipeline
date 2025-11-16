
  
    

  create  table "dbt_db"."dbt_default_silver"."dim_customer__dbt_tmp"
  
  
    as
  
  (
    with customer_data as (
        select
           customer_id,
            first_name,
            last_name,
            email,
            replace(signup_date::text, '-', '')::int as signup_date_key
            
        from "dbt_db"."dbt_default_bronze"."customer"
    )


select *
from customer_data
  );
  