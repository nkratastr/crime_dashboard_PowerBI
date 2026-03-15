# Crime Dashboard - Power BI

Een crime dashboard gebouwd met:
- **Databron**: CBS / Politie open data
- **Data warehouse**: Snowflake
- **Transformaties**: dbt
- **Visualisatie**: Power BI

## Projectstructuur

```
crime_dashboard_PowerBI/
├── data/              # Ruwe data van CBS/politie
├── dbt/               # dbt modellen en transformaties
│   ├── models/
│   └── seeds/
├── snowflake/         # SQL scripts voor Snowflake setup
├── powerbi/           # Power BI bestanden (.pbix)
└── docs/              # Documentatie
```
