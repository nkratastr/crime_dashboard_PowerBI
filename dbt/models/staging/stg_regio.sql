with source as (
    select * from {{ source('raw', 'DIM_REGIO') }}
)

select
    trim(key)                           as regio_code,
    trim(title)                         as regio_naam,
    case left(trim(key), 2)
        when 'GM' then 'Gemeente'
        when 'PV' then 'Provincie'
        when 'LD' then 'Landsdeel'
        when 'RE' then 'Regio'
        when 'NL' then 'Nederland'
        else 'Overig'
    end                                 as regio_type
from source
