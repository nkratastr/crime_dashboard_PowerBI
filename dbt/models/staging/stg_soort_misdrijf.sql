with source as (
    select * from {{ source('raw', 'DIM_SOORT_MISDRIJF') }}
)

select
    trim(key)           as soort_misdrijf_code,
    trim(title)         as soort_misdrijf,
    trim(description)   as omschrijving,
    category_group_id
from source
