"""
Haalt criminaliteitsdata op van CBS StatLine open API
Dataset: Geregistreerde criminaliteit; soort misdrijf, regio
URL: https://opendata.cbs.nl/statline/portal.html?_la=nl&_catalog=CBS&tableId=83648NED
"""

import requests
import pandas as pd
import os

BASE_URL = "https://opendata.cbs.nl/ODataApi/odata/83648NED"
RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")


def fetch_table(endpoint: str, page_size: int = 5000) -> list:
    """Haalt alle pagina's op van een OData endpoint met paginering."""
    results = []
    skip = 0

    while True:
        url = f"{BASE_URL}/{endpoint}?$top={page_size}&$skip={skip}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        batch = data.get("value", [])
        results.extend(batch)
        print(f"     {skip + len(batch)} rijen opgehaald...", end="\r")

        if len(batch) < page_size:
            break
        skip += page_size

    return results


def main():
    os.makedirs(RAW_DIR, exist_ok=True)

    print("Ophalen: feiten (criminaliteitscijfers)...")
    feiten = fetch_table("TypedDataSet")
    df_feiten = pd.DataFrame(feiten)
    feiten_path = os.path.join(RAW_DIR, "criminaliteit_observations.csv")
    df_feiten.to_csv(feiten_path, index=False)
    print(f"  -> {len(df_feiten)} rijen opgeslagen in {feiten_path}")

    print("Ophalen: dimensietabellen...")

    for dim in ["SoortMisdrijf", "RegioS", "Perioden"]:
        print(f"  -> {dim}...")
        data = fetch_table(dim)
        df = pd.DataFrame(data)
        path = os.path.join(RAW_DIR, f"dim_{dim.lower()}.csv")
        df.to_csv(path, index=False)
        print(f"     {len(df)} rijen opgeslagen in {path}")

    print("\nKlaar! Alle data staat in data/raw/")


if __name__ == "__main__":
    main()
