with source as (
    select * from {{ source('raw', 'CRIMINALITEIT_OBSERVATIONS') }}
)

select
    id,
    trim(soort_misdrijf)                    as soort_misdrijf_code,
    trim(regio)                             as regio_code,
    trim(periode)                           as periode_code,
    totaal_geregistreerde_misdrijven        as totaal_geregistreerd,
    geregistreerde_misdrijven_relatief      as pct_geregistreerd,
    geregistreerde_misdrijven_per_1000      as per_1000_inwoners,
    totaal_opgehelderde_misdrijven          as totaal_opgehelderd,
    opgehelderde_misdrijven_relatief        as pct_opgehelderd,
    registraties_van_verdachten             as verdachten
from source
