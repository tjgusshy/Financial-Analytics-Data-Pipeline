
  create view "dbt_db"."public"."stg_sample_data__dbt_tmp"
    
    
  as (
    -- Sample staging model


select
    1 as id,
    'Sample Record' as name,
    current_timestamp as created_at

union all

select
    2 as id,
    'Another Record' as name,
    current_timestamp as created_at
  );