select * 
from {{ source('moneybox_raw', 'raw_products') }}