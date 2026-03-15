with source as (
    select * from {{ source('raw', 'DIM_REGIO') }}
)

select
    trim(key)       as regio_code,
    trim(title)     as regio_naam
from source
