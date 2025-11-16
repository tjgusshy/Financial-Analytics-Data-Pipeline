
  
    

  create  table "dbt_db"."public"."fct_sample_processed__dbt_tmp"
  
  
    as
  
  (
    -- Sample mart model


select
    id,
    upper(name) as name_upper,
    created_at,
    current_timestamp as processed_at
from "dbt_db"."public"."stg_sample_data"
where id is not null
  );
  