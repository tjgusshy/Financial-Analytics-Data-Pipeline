
  
    

  create  table "dbt_db"."dbt_default_bronze"."customer__dbt_tmp"
  
  
    as
  
  (
    select * 
from "dbt_db"."public"."raw_customers"
  );
  