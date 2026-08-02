"""
ingest.py — PSA Poverty Statistics Ingestion Script
Philippine Regional Poverty Divergence Tracker
DEP Program — Phase 1, Milestone 2

Purpose:
    Pulls poverty statistics tables from the PSA OpenSTAT PX-Web API
    and saves them as dated CSV files in data/raw/.

Source:
    PSA Full Year Official Poverty Statistics
    https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__1E__FY/

Usage:
    python scripts/ingest.py

Output:
    data/raw/psa_<table_id>_<YYYY-MM-DD>.csv  for each table
    data/raw/data_dictionary_<YYYY-MM-DD>.csv  field reference
"""

import os
import json
import requests
import pandas as pd
from datetime import date

# ── Configuration ──────────────────────────────────────────────────────────────

BASE_URL = "https://openstat.psa.gov.ph/PXWeb/api/v1/en/DB/DB__1E__FY/"
RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PULL_DATE = date.today().isoformat()  # e.g. 2025-08-01

# Tables to ingest — (table_id, filename_label, description)
TABLES = [
    (
        "0012E4DFTE0.px",
        "table1_families_incidence",
        "Annual Per Capita Poverty Threshold and Poverty Incidence Among Families by Region and Province",
    ),
    (
        "0012E4DFTE1.px",
        "table1a_families_incidence_huc",
        "Annual Per Capita Poverty Threshold and Poverty Incidence Among Families by Region Province and HUC",
    ),
    (
        "0012E4DFTE2.px",
        "table2_population_incidence",
        "Annual Per Capita Poverty Threshold and Poverty Incidence Among Population by Region and Province",
    ),
    (
        "0012E4DFTE3.px",
        "table2a_population_incidence_huc",
        "Annual Per Capita Poverty Threshold and Poverty Incidence Among Population by Region Province and HUC",
    ),
    (
        "0012E4DFTE9.px",
        "table11_poverty_gap",
        "Poverty Gap with Measures of Precision by Region and Province",
    ),
    (
        "0012E4DFTE10.px",
        "table12_severity",
        "Severity of Poverty with Measures of Precision by Region and Province",
    ),
    (
        "0012E4DFTE11.px",
        "table13_luzon_visayas_mindanao",
        "Poverty Incidence among Families and Population in Luzon Visayas and Mindanao",
    ),
]

# ── Helpers ────────────────────────────────────────────────────────────────────

def ensure_raw_dir():
    """Create data/raw/ if it does not exist."""
    os.makedirs(RAW_DIR, exist_ok=True)
    print(f"[INFO] Raw data directory: {os.path.abspath(RAW_DIR)}")


def fetch_table(table_id: str) -> dict:
    """
    Query the PSA OpenSTAT PX-Web API for a specific table.
    Returns the full JSON response as a dict.
    """
    url = BASE_URL + table_id
    print(f"[FETCH] {url}")

    # Request all available data by posting an empty selection
    payload = {"query": [], "response": {"format": "json"}}

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error for {table_id}: {e}")
        return None
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Cannot connect to PSA OpenSTAT. Check your internet connection.")
        return None
    except requests.exceptions.Timeout:
        print(f"[ERROR] Request timed out for {table_id}.")
        return None


def parse_pxweb_json(data: dict) -> pd.DataFrame:
    """
    Convert a PX-Web JSON response into a flat pandas DataFrame.
    PX-Web returns columns and data separately — this joins them.
    """
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
            value_cols = col_names[len(keys) :]
            for vc, val in zip(value_cols, values):
                record[vc] = val
            records.append(record)

        return pd.DataFrame(records)

    except (KeyError, TypeError) as e:
        print(f"[ERROR] Failed to parse PX-Web response: {e}")
        return pd.DataFrame()


def save_csv(df: pd.DataFrame, filename_label: str) -> str:
    """
    Save DataFrame to data/raw/ with source name and pull date in filename.
    Returns the full file path.
    """
    filename = f"psa_{filename_label}_{PULL_DATE}.csv"
    filepath = os.path.join(RAW_DIR, filename)
    df.to_csv(filepath, index=False, encoding="utf-8-sig")
    print(f"[SAVED] {filepath} — {len(df)} rows, {len(df.columns)} columns")
    return filepath


def build_data_dictionary(results: list) -> pd.DataFrame:
    """
    Build a data dictionary from all ingested tables.
    Documents each field, its table source, and inferred type.
    """
    entries = []
    for label, description, df in results:
        if df.empty:
            continue
        for col in df.columns:
            sample_vals = df[col].dropna().astype(str).head(3).tolist()
            inferred_type = "numeric" if df[col].dtype in ["float64", "int64"] else "text"
            entries.append(
                {
                    "table": label,
                    "table_description": description,
                    "field_name": col,
                    "inferred_type": inferred_type,
                    "sample_values": " | ".join(sample_vals),
                    "notes": "",
                }
            )
    return pd.DataFrame(entries)


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("PSA Poverty Statistics Ingestion Script")
    print(f"Pull date : {PULL_DATE}")
    print(f"Source    : {BASE_URL}")
    print("=" * 60)

    ensure_raw_dir()

    results = []

    for table_id, label, description in TABLES:
        print(f"\n── Table: {label}")
        raw = fetch_table(table_id)
        df = parse_pxweb_json(raw)

        if df.empty:
            print(f"[SKIP] No data returned for {label}.")
            results.append((label, description, df))
            continue

        save_csv(df, label)
        results.append((label, description, df))

    # Build and save data dictionary
    print("\n── Building data dictionary...")
    dict_df = build_data_dictionary(results)
    if not dict_df.empty:
        dict_path = os.path.join(RAW_DIR, f"data_dictionary_{PULL_DATE}.csv")
        dict_df.to_csv(dict_path, index=False, encoding="utf-8-sig")
        print(f"[SAVED] {dict_path} — {len(dict_df)} field entries")

    print("\n" + "=" * 60)
    print("Ingestion complete.")
    print(f"Files saved to: {os.path.abspath(RAW_DIR)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
