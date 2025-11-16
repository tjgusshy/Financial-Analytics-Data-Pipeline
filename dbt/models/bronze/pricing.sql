select * 
from {{ source('moneybox_raw', 'raw_pricing') }}