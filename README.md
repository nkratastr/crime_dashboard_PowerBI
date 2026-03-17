# Crime Dashboard - Power BI

Een crime dashboard gebouwd met Nederlandse open data (CBS / Politie), getransformeerd via dbt en gevisualiseerd in Power BI.

## Tech Stack

| Laag | Tool |
|------|------|
| Databron | CBS / Politie open data |
| Data warehouse | Snowflake |
| Transformaties | dbt (dbt-snowflake) |
| Visualisatie | Power BI |
| Taal | Python 3.12 |

## Projectstructuur

```
crime_dashboard_PowerBI/
├── data/
│   ├── raw/               # Ruwe CBS/politie data (niet in git)
│   └── processed/         # Verwerkte data (niet in git)
├── dbt/                   # dbt project
│   ├── models/
│   │   ├── staging/       # Bronlaag modellen (stg_*)
│   │   └── marts/         # Eindlaag modellen (dim_*, fct_*)
│   ├── seeds/
│   └── profiles.yml       # dbt Snowflake verbinding (niet in git)
├── snowflake/
│   ├── 01_setup.sql       # Aanmaken database, schema's en rollen
│   ├── 02_tables.sql      # Tabel definities
│   └── load_data.py       # Data laden vanuit CSV naar Snowflake RAW schema
├── powerbi/               # Power BI bestanden (.pbix)
├── docs/                  # Documentatie
├── .env.example           # Voorbeeld omgevingsvariabelen
└── requirements.txt       # Python dependencies
```

## Installatie & Setup

### 1. Python omgeving

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Snowflake configuratie

Maak een `.env` bestand aan op basis van `.env.example`:

```bash
cp .env.example .env
```

Vul de volgende waarden in:

```env
SNOWFLAKE_ACCOUNT=<jouw-account-identifier>
SNOWFLAKE_USER=<jouw-gebruikersnaam>
SNOWFLAKE_PASSWORD=<jouw-wachtwoord>
SNOWFLAKE_ROLE=CRIME_DASHBOARD_ROLE
SNOWFLAKE_WAREHOUSE=CRIME_DASHBOARD_WH
SNOWFLAKE_DATABASE=CRIME_DASHBOARD_DB
SNOWFLAKE_SCHEMA=RAW
```

Voer daarna de setup scripts uit in Snowflake (in volgorde):

```sql
-- In Snowflake worksheet:
-- 1. Eerst 01_setup.sql (database, warehouse, rollen)
-- 2. Dan 02_tables.sql (tabellen)
```

### 3. dbt configuratie

Maak `dbt/profiles.yml` aan (wordt genegeerd door git):

```yaml
crime_dashboard:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: "{{ env_var('SNOWFLAKE_ACCOUNT') }}"
      user: "{{ env_var('SNOWFLAKE_USER') }}"
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      role: "{{ env_var('SNOWFLAKE_ROLE') }}"
      warehouse: "{{ env_var('SNOWFLAKE_WAREHOUSE') }}"
      database: "{{ env_var('SNOWFLAKE_DATABASE') }}"
      schema: DBT_DEV
      threads: 4
```

### 4. Data laden

```bash
python snowflake/load_data.py
```

### 5. dbt modellen uitvoeren

```bash
cd dbt
dbt deps
dbt run
dbt test
```

## Snowflake structuur

```
CRIME_DASHBOARD_DB
├── RAW          # Ruwe data geladen via load_data.py
├── DBT_DEV      # dbt ontwikkel schema
└── DBT_PROD     # dbt productie schema
```

## Regio typen

De data bevat twee regio niveaus:
- `gemeente` — gemeentelijk niveau
- `provincie` — provinciaal niveau

Het veld `regio_type` wordt gebruikt om onderscheid te maken in de modellen.
