with feiten as (
    select * from {{ ref('stg_criminaliteit') }}
),

misdrijf as (
    select * from {{ ref('stg_soort_misdrijf') }}
),

regio as (
    select * from {{ ref('stg_regio') }}
),

periode as (
    select * from {{ ref('stg_periode') }}
)

select
    f.id,
    p.jaar_int                          as jaar,
    p.status                            as jaar_status,
    r.regio_naam,
    r.regio_type,
    m.soort_misdrijf,
    m.omschrijving                      as misdrijf_omschrijving,
    f.totaal_geregistreerd,
    f.pct_geregistreerd,
    f.per_1000_inwoners,
    f.totaal_opgehelderd,
    f.pct_opgehelderd,
    f.verdachten
from feiten f
left join misdrijf m on f.soort_misdrijf_code = m.soort_misdrijf_code
left join regio    r on f.regio_code           = r.regio_code
left join periode  p on f.periode_code         = p.periode_code
