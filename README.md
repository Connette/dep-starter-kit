# Philippine Regional Poverty Divergence Tracker
**24-Week Data Analytics Foundations Program — Froncoyz Verano**

---

## Project Overview
This project tracks regional poverty convergence across all 17 Philippine regions
using official PSA open data from 2015 to 2023.

**Central question:** Which Philippine regions are closing the poverty gap fastest —
and which ones are being left behind?

A secondary lens follows Caraga (Region XIII), which had one of the highest poverty
incidence rates in 2015 and has since posted significant reductions.

---
## Milestones

| Milestone | Description | Status |
|---|---|---|
| M0 | Problem Statement | ✅ Complete |
| M1 | Data Source Discovery & Feasibility Check | ✅ Complete |

---
## Repo Structure

dep-starter-kit/
├── data/
│   ├── raw/          # Unmodified CSV exports from PSA OpenSTAT
│   └── processed/    # Cleaned, analysis-ready files
├── notebooks/        # Jupyter notebooks for exploration and analysis
├── output/           # Chart exports and report outputs
├── scripts/          # Python cleaning and analysis scripts
├── README.md         # This file
└── requirements.txt  # Python dependencies


---

## Data Source

### Primary Source
- **Name:** PSA Full Year Official Poverty Statistics — OpenSTAT Portal
- **URL:** https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__1E__FY/?tablelist=true
- **Format:** CSV/XLSX, exported directly from the PX-Web portal, no login required
- **Coverage:** All 17 regions + provinces; survey years 2015, 2018, 2021, 2023; national/regional/provincial/HUC level
- **Why it fits:** Authoritative source for poverty incidence, thresholds, income gap, and magnitude of poor by region — every KPI in the problem statement is exportable directly from here.
- **Known limitations:** 2015 tables use 2006-based CPI vs. 2012-based CPI from 2018+ (thresholds not directly comparable); small-province estimates have unreliable coefficients of variation; magnitude tables lag behind incidence tables in coverage year.

### Fallback Source
- **Name:** PSA Philippine Statistical Yearbook (PSY), Chapter 2
- **URL:** https://psa.gov.ph/system/files/psy/2_2023.xlsx
- **Format:** XLSX, single-file direct download
- **Coverage:** National/regional poverty and income tables, published annually
- **Why it could still work:** Same underlying PSA data, delivered through a completely different access path (static file vs. portal), so a portal outage doesn't take out both sources.
- **Known limitations:** Weaker provincial-level detail; merged cells/footnotes require more cleaning; lags one FIES cycle behind.

---



### Programmatic Ingestion
Data is pulled via `scripts/ingest.py` using the World Bank Indicators API v2,
which sources Philippine poverty statistics directly from PSA official data.
Run `python scripts/ingest.py` to fetch latest data into `data/raw/`.



## Setup
```bash
git clone https://github.com/Froncoyz/dep-starter-kit.git
cd dep-starter-kit
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```
