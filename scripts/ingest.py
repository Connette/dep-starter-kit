"""
ingest.py - PSA Poverty Statistics Ingestion Script
Philippine Regional Poverty Divergence Tracker
DEP Program - Phase 1, Milestone 2

Purpose:
    Pulls Philippine poverty indicators from the World Bank API
    (which sources data from PSA/official government statistics)
    and saves dated CSV files to data/raw/.

Primary Source (M1-confirmed):
    PSA Full Year Official Poverty Statistics
    https://psa.gov.ph/statistics/poverty

API Source (programmatic access):
    World Bank Indicators API v2 - Philippine poverty indicators
    https://api.worldbank.org/v2/country/PH/indicator/

    Note: World Bank poverty data for the Philippines is sourced
    directly from PSA official statistics (FIES-based estimates).
    This API provides programmatic access to the same underlying
    data published by PSA.

Usage:
    python scripts/ingest.py

Output:
<<<<<<< HEAD
    data/raw/psa_worldbank_<indicator>_<YYYY-MM-DD>.csv
    data/raw/psa_worldbank_data_dictionary_<YYYY-MM-DD>.csv
=======
    data/raw/psa_<table_label>_<YYYY-MM-DD>.csv  for each table
    data/raw/data_dictionary_<YYYY-MM-DD>.csv     field reference
>>>>>>> f8700e762702cb22a7f66835c85ca60ad5878322
"""

import os
import requests
import pandas as pd
from datetime import date

# -- Configuration -------------------------------------------------------------

<<<<<<< HEAD
RAW_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw"
)
PULL_DATE = date.today().isoformat()
BASE_URL = "https://api.worldbank.org/v2/country/PH/indicator"

# World Bank indicators for Philippine poverty analysis
# All sourced from PSA official statistics via World Bank Poverty and
# Inequality Platform
INDICATORS = [
    (
        "SI.POV.NAHC",
        "poverty_incidence_national",
        "Poverty headcount ratio at national poverty lines pct of population Philippines PSA-sourced",
    ),
    (
        "SI.POV.GAPS",
        "poverty_gap_national",
        "Poverty gap at national poverty lines pct Philippines PSA-sourced",
    ),
    (
        "SI.POV.DDAY",
        "poverty_incidence_215usd",
        "Poverty headcount ratio at USD 2.15 per day 2017 PPP pct of population Philippines",
    ),
    (
        "SI.DST.FRST.20",
        "income_share_bottom20pct",
        "Income share held by lowest 20 percent Philippines",
    ),
    (
        "SI.DST.10TH.10",
        "income_share_bottom10pct",
        "Income share held by lowest 10 percent Philippines",
    ),
    (
        "NY.GDP.PCAP.CD",
        "gdp_per_capita_usd",
        "GDP per capita current USD Philippines context indicator",
    ),
    (
        "SP.POP.TOTL",
        "population_total",
        "Total population Philippines denominator for magnitude estimates",
=======
BASE_URL = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/DB__1E__FY/"
RAW_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
PULL_DATE = date.today().isoformat()  # e.g. 2026-08-02

# Confirmed table IDs from PSA OpenSTAT (verified via portal URLs)
TABLES = [
    (
        "0011E3DF010.px",
        "table1_families_incidence",
        "Annual Per Capita Poverty Threshold and Poverty Incidence Among Families by Region and Province 2018 2021 2023",
    ),
    (
        "0031E3DF020.px",
        "table2_population_incidence",
        "Annual Per Capita Poverty Threshold and Poverty Incidence Among Population by Region and Province 2018 2021 2023",
    ),
    (
        "0091E3DF050.px",
        "table5_magnitude_families",
        "Magnitude of Poor Families with Measures of Precision by Region and Province 2015 2018 2021",
    ),
    (
        "0111E3DF060.px",
        "table6_magnitude_population",
        "Magnitude of Poor Population with Measures of Precision by Region and Province 2015 2018 2021",
>>>>>>> f8700e762702cb22a7f66835c85ca60ad5878322
    ),
]

# -- Helpers -------------------------------------------------------------------

def ensure_raw_dir():
    os.makedirs(RAW_DIR, exist_ok=True)
    print(f"[INFO] Raw data directory: {os.path.abspath(RAW_DIR)}")


<<<<<<< HEAD
def fetch_indicator(indicator_code, per_page=100, date_range="2000:2024"):
    """
    Fetch a World Bank indicator for the Philippines.
    Returns a list of data records.
    """
    url = (
        f"{BASE_URL}/{indicator_code}"
        f"?format=json&per_page={per_page}&date={date_range}"
    )
    print(f"[FETCH] {url}")
=======
def fetch_table(table_id: str) -> dict:
    url = BASE_URL + table_id
    print(f"[FETCH] {url}")
    payload = {"query": [], "response": {"format": "json"}}
>>>>>>> f8700e762702cb22a7f66835c85ca60ad5878322
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        # World Bank API returns [metadata, data_list]
        if not isinstance(data, list) or len(data) < 2:
            print(f"[ERROR] Unexpected response format for {indicator_code}")
            return None

        records = data[1]
        if records is None:
            print(f"[WARN] No data available for {indicator_code}")
            return None

        return records

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error for {indicator_code}: {e}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to World Bank API. Check internet.")
        return None
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out for {indicator_code}.")
        return None
    except Exception as e:
        print(f"[ERROR] Unexpected error for {indicator_code}: {e}")
        return None


<<<<<<< HEAD
def parse_records(records, indicator_code, description):
    """Convert World Bank API records to a flat DataFrame."""
    if not records:
        return pd.DataFrame()

    rows = []
    for r in records:
        rows.append({
            "indicator_code": indicator_code,
            "indicator_name": r.get("indicator", {}).get("value", ""),
            "country": r.get("country", {}).get("value", "Philippines"),
            "country_code": r.get("countryiso3code", "PHL"),
            "year": r.get("date", ""),
            "value": r.get("value", ""),
            "unit": r.get("unit", ""),
            "obs_status": r.get("obs_status", ""),
            "source": "World Bank API / PSA Philippines",
            "pull_date": PULL_DATE,
            "description": description,
        })

    df = pd.DataFrame(rows)
    # Sort by year descending
    df = df.sort_values("year", ascending=False).reset_index(drop=True)
    return df


def save_csv(df, label):
    filename = f"psa_worldbank_{label}_{PULL_DATE}.csv"
=======
def parse_pxweb_json(data: dict) -> pd.DataFrame:
    if data is None:
        return pd.DataFrame()
    try:
        columns = data["columns"]
        rows = data["data"]
        col_names = [c["text"] for c in columns]
        records = []
        for row in rows:
            keys = row["key"]
            values = row["values"]
            record = dict(zip(col_names[: len(keys)], keys))
            value_cols = col_names[len(keys):]
            for vc, val in zip(value_cols, values):
                record[vc] = val
            records.append(record)
        return pd.DataFrame(records)
    except (KeyError, TypeError) as e:
        print(f"[ERROR] Failed to parse PX-Web response: {e}")
        return pd.DataFrame()


def save_csv(df: pd.DataFrame, filename_label: str) -> str:
    filename = f"psa_{filename_label}_{PULL_DATE}.csv"
>>>>>>> f8700e762702cb22a7f66835c85ca60ad5878322
    filepath = os.path.join(RAW_DIR, filename)
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"[SAVED] {filename} - {len(df)} rows x {len(df.columns)} cols")
    return filepath


<<<<<<< HEAD
def build_data_dictionary(results):
    """Build a field-level data dictionary from all ingested tables."""
=======
def build_data_dictionary(results: list) -> pd.DataFrame:
>>>>>>> f8700e762702cb22a7f66835c85ca60ad5878322
    entries = []
    for label, description, df in results:
        if df is None or df.empty:
            continue
        for col in df.columns:
<<<<<<< HEAD
            samples = df[col].dropna().astype(str).head(3).tolist()
            try:
                pd.to_numeric(df[col])
                dtype = "numeric"
            except Exception:
                dtype = "text"
            entries.append({
                "table": f"psa_worldbank_{label}",
                "field_name": col,
                "type": dtype,
                "description": description if col == "value" else "",
                "sample_values": " | ".join(samples),
=======
            sample_vals = df[col].dropna().astype(str).head(3).tolist()
            try:
                pd.to_numeric(df[col])
                inferred_type = "numeric"
            except (ValueError, TypeError):
                inferred_type = "text"
            entries.append({
                "table": label,
                "table_description": description,
                "field_name": col,
                "inferred_type": inferred_type,
                "sample_values": " | ".join(sample_vals),
                "notes": "",
>>>>>>> f8700e762702cb22a7f66835c85ca60ad5878322
            })
    return pd.DataFrame(entries)


# -- Main ----------------------------------------------------------------------

def main():
    print("=" * 60)
    print("PSA Poverty Statistics Ingestion Script")
    print(f"Pull date  : {PULL_DATE}")
    print(f"API source : api.worldbank.org/v2 (PSA-sourced data)")
    print(f"Country    : Philippines (PH / PHL)")
    print("=" * 60)

    ensure_raw_dir()
    results = []
    success_count = 0

    for code, label, description in INDICATORS:
        print(f"\n-- Indicator: {code} ({label})")
        records = fetch_indicator(code)
        df = parse_records(records, code, description)

        if df.empty:
            print(f"[SKIP] No data for {label}")
            results.append((label, description, None))
            continue

        save_csv(df, label)
        results.append((label, description, df))
        success_count += 1

<<<<<<< HEAD
    # Build and save data dictionary
    print("\n-- Building data dictionary...")
    dd = build_data_dictionary(results)
    if not dd.empty:
        dd_path = os.path.join(
            RAW_DIR, f"psa_worldbank_data_dictionary_{PULL_DATE}.csv"
        )
        dd.to_csv(dd_path, index=False, encoding="utf-8-sig")
        print(f"[SAVED] psa_worldbank_data_dictionary_{PULL_DATE}.csv - {len(dd)} entries")
=======
    # Build and save data dictionary CSV
    print("\n── Building data dictionary CSV...")
    dict_df = build_data_dictionary(results)
    if not dict_df.empty:
        dict_path = os.path.join(RAW_DIR, f"data_dictionary_{PULL_DATE}.csv")
        dict_df.to_csv(dict_path, index=False, encoding="utf-8-sig")
        print(f"[SAVED] {dict_path} — {len(dict_df)} field entries")
    else:
        print("[WARN] No data was ingested — data dictionary is empty.")
>>>>>>> f8700e762702cb22a7f66835c85ca60ad5878322

    print("\n" + "=" * 60)
    print(f"Ingestion complete. {success_count}/{len(INDICATORS)} indicators pulled.")
    print(f"Output: {os.path.abspath(RAW_DIR)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
