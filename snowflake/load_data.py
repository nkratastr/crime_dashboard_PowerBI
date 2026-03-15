"""
Laadt ruwe CBS data vanuit data/raw/ naar Snowflake RAW schema.
Vereist: .env bestand met Snowflake credentials
"""

import os
import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
from dotenv import load_dotenv

load_dotenv()

COLUMN_MAP = {
    "criminaliteit_observations.csv": {
        "table": "CRIMINALITEIT_OBSERVATIONS",
        "rename": {
            "ID": "ID",
            "SoortMisdrijf": "SOORT_MISDRIJF",
            "RegioS": "REGIO",
            "Perioden": "PERIODE",
            "TotaalGeregistreerdeMisdrijven_1": "TOTAAL_GEREGISTREERDE_MISDRIJVEN",
            "GeregistreerdeMisdrijvenRelatief_2": "GEREGISTREERDE_MISDRIJVEN_RELATIEF",
            "GeregistreerdeMisdrijvenPer1000Inw_3": "GEREGISTREERDE_MISDRIJVEN_PER_1000",
            "TotaalOpgehelderdeMisdrijven_4": "TOTAAL_OPGEHELDERDE_MISDRIJVEN",
            "OpgehelderdeMisdrijvenRelatief_5": "OPGEHELDERDE_MISDRIJVEN_RELATIEF",
            "RegistratiesVanVerdachten_6": "REGISTRATIES_VAN_VERDACHTEN",
        }
    },
    "dim_soortmisdrijf.csv": {
        "table": "DIM_SOORT_MISDRIJF",
        "rename": {
            "Key": "KEY",
            "Title": "TITLE",
            "Description": "DESCRIPTION",
            "CategoryGroupID": "CATEGORY_GROUP_ID",
        }
    },
    "dim_regios.csv": {
        "table": "DIM_REGIO",
        "rename": {
            "Key": "KEY",
            "Title": "TITLE",
            "Description": "DESCRIPTION",
            "CategoryGroupID": "CATEGORY_GROUP_ID",
        }
    },
    "dim_perioden.csv": {
        "table": "DIM_PERIODE",
        "rename": {
            "Key": "KEY",
            "Title": "TITLE",
            "Description": "DESCRIPTION",
            "Status": "STATUS",
        }
    },
}

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")


def connect():
    return snowflake.connector.connect(
        account=os.environ["SNOWFLAKE_ACCOUNT"],
        user=os.environ["SNOWFLAKE_USER"],
        password=os.environ["SNOWFLAKE_PASSWORD"],
        role=os.environ["SNOWFLAKE_ROLE"],
        warehouse=os.environ["SNOWFLAKE_WAREHOUSE"],
        database=os.environ["SNOWFLAKE_DATABASE"],
        schema=os.environ["SNOWFLAKE_SCHEMA"],
    )


def main():
    conn = connect()
    print("Verbonden met Snowflake.")

    for filename, config in COLUMN_MAP.items():
        path = os.path.join(RAW_DIR, filename)
        print(f"\nLaden: {filename} -> {config['table']}...")

        df = pd.read_csv(path)
        df = df.rename(columns=config["rename"])
        df = df[list(config["rename"].values())]

        success, nchunks, nrows, _ = write_pandas(
            conn, df, config["table"], auto_create_table=False
        )
        print(f"  -> {nrows} rijen geladen in {nchunks} chunks")

    conn.close()
    print("\nKlaar!")


if __name__ == "__main__":
    main()
