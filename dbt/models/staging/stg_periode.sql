with source as (
    select * from {{ source('raw', 'DIM_PERIODE') }}
)

select
    trim(key)                               as periode_code,
    trim(title)                             as jaar,
    cast(trim(title) as integer)            as jaar_int,
    trim(status)                            as status
from source
