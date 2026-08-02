# Data Dictionary — Philippine Regional Poverty Divergence Tracker
**Source:** PSA Full Year Official Poverty Statistics via OpenSTAT
**URL:** https://openstat.psa.gov.ph/PXWeb/pxweb/en/DB/DB__1E__FY/
**Last updated:** 2023 FIES cycle (released September 2024)

---

## Entity Relationship Overview

```
PSA_REGION ──< PSA_PROVINCE ──< PSA_HUC
     │               │
     │               └──< POVERTY_INCIDENCE_FAMILIES
     │               └──< POVERTY_INCIDENCE_POPULATION
     │               └──< POVERTY_THRESHOLD
     │               └──< INCOME_GAP
     │               └──< POVERTY_GAP
     │               └──< SEVERITY_OF_POVERTY
     │
     └──< MINDANAO_VISAYAS_LUZON_GROUPING
```

All tables share `Region` and `Province` as the primary join keys.
Survey year (`2018`, `2021`, `2023`) is the time dimension across all tables.

---

## Table 1 — Poverty Incidence Among Families + Poverty Threshold
**File:** `psa_table1_families_incidence_<date>.csv`
**Grain:** One row per province per survey year

| Field | Type | Description | Example |
|---|---|---|---|
| `Region` | text | PSA region name | `CARAGA` |
| `Province` | text | Province or national/regional summary | `Agusan del Norte` |
| `Year` | integer | Survey year (FIES cycle) | `2023` |
| `Annual_Per_Capita_Poverty_Threshold` | numeric (PhP) | Minimum annual income per person to escape poverty | `28,709` |
| `Poverty_Incidence_Among_Families_pct` | numeric (%) | Share of families below poverty threshold | `15.4` |
| `Standard_Error_PI_Families` | numeric | Statistical precision measure for poverty incidence | `1.2` |
| `Coefficient_of_Variation_PI_Families` | numeric (%) | CV > 20% = unreliable estimate; use with caution | `7.8` |
| `Lower_95CI_PI_Families` | numeric (%) | Lower bound of 95% confidence interval | `12.9` |
| `Upper_95CI_PI_Families` | numeric (%) | Upper bound of 95% confidence interval | `17.9` |

**Notes:**
- Poverty threshold uses 2012-based CPI for 2018, 2021, and 2023; 2006-based CPI for 2015. Do not compare peso values across this break.
- CV > 20% rows are flagged by PSA as statistically unreliable. Use `Table 15 — Province Groupings` for ranking small provinces.

---

## Table 1a — Poverty Incidence Among Families (HUC Level)
**File:** `psa_table1a_families_incidence_huc_<date>.csv`
**Grain:** One row per highly urbanized city per survey year
**Available from:** 2018 onward only (not 2015)

| Field | Type | Description | Example |
|---|---|---|---|
| `Region` | text | PSA region name | `Region XIII` |
| `Province` | text | Province the HUC belongs to | `Agusan del Norte` |
| `HUC` | text | Highly Urbanized City name | `Butuan City` |
| `Year` | integer | Survey year | `2023` |
| `Annual_Per_Capita_Poverty_Threshold` | numeric (PhP) | City-level poverty threshold | `27,450` |
| `Poverty_Incidence_Among_Families_pct` | numeric (%) | City-level family poverty incidence | `12.2` |
| `Standard_Error_PI_Families` | numeric | Standard error | `1.8` |
| `Coefficient_of_Variation_PI_Families` | numeric (%) | CV for reliability assessment | `14.8` |

**Notes:**
- Butuan City is the only HUC in Caraga and a key reference point for this project. It dropped from 22.6% (2021) to 12.2% (2023).

---

## Table 2 — Poverty Incidence Among Population
**File:** `psa_table2_population_incidence_<date>.csv`
**Grain:** One row per province per survey year

| Field | Type | Description | Example |
|---|---|---|---|
| `Region` | text | PSA region name | `CARAGA` |
| `Province` | text | Province name | `Surigao del Sur` |
| `Year` | integer | Survey year | `2021` |
| `Annual_Per_Capita_Poverty_Threshold` | numeric (PhP) | Population-level threshold | `27,003` |
| `Poverty_Incidence_Among_Population_pct` | numeric (%) | Share of individuals below poverty threshold | `19.2` |
| `Standard_Error_PI_Population` | numeric | Standard error | `1.4` |
| `Coefficient_of_Variation_PI_Population` | numeric (%) | CV for reliability | `7.3` |
| `Lower_95CI_PI_Population` | numeric (%) | Lower confidence bound | `16.4` |
| `Upper_95CI_PI_Population` | numeric (%) | Upper confidence bound | `22.0` |

**Notes:**
- Population incidence is always slightly higher than family incidence because larger (poorer) families have more members per poor household.

---

## Table 11 — Poverty Gap
**File:** `psa_table11_poverty_gap_<date>.csv`
**Grain:** One row per province per survey year

| Field | Type | Description | Example |
|---|---|---|---|
| `Region` | text | PSA region name | `CARAGA` |
| `Province` | text | Province name | `Dinagat Islands` |
| `Year` | integer | Survey year | `2023` |
| `Poverty_Gap_pct` | numeric (%) | Average income shortfall as % of poverty threshold | `5.1` |
| `Standard_Error_PG` | numeric | Standard error | `0.8` |
| `Coefficient_of_Variation_PG` | numeric (%) | CV for reliability | `15.7` |
| `Lower_95CI_PG` | numeric (%) | Lower confidence bound | `3.5` |
| `Upper_95CI_PG` | numeric (%) | Upper confidence bound | `6.7` |

**Notes:**
- A declining poverty gap means poor families are not just fewer in number but also closer to the threshold — shallower poverty.
- Used alongside poverty incidence to assess whether improvements reflect genuine welfare gains or just families crossing the threshold line.

---

## Table 12 — Severity of Poverty
**File:** `psa_table12_severity_<date>.csv`
**Grain:** One row per province per survey year

| Field | Type | Description | Example |
|---|---|---|---|
| `Region` | text | PSA region name | `CARAGA` |
| `Province` | text | Province name | `Agusan del Sur` |
| `Year` | integer | Survey year | `2023` |
| `Severity_of_Poverty_pct` | numeric (%) | Weighted measure of depth and inequality among the poor | `2.1` |
| `Standard_Error_SP` | numeric | Standard error | `0.4` |
| `Coefficient_of_Variation_SP` | numeric (%) | CV for reliability | `19.0` |

---

## Table 13 — Poverty Incidence by Island Group
**File:** `psa_table13_luzon_visayas_mindanao_<date>.csv`
**Grain:** One row per island group per survey year

| Field | Type | Description | Example |
|---|---|---|---|
| `Island_Group` | text | Luzon, Visayas, or Mindanao | `Mindanao` |
| `Year` | integer | Survey year | `2023` |
| `Poverty_Incidence_Families_pct` | numeric (%) | Island group family poverty incidence | `21.0` |
| `Poverty_Incidence_Population_pct` | numeric (%) | Island group population poverty incidence | `24.5` |

**Notes:**
- Caraga is part of Mindanao. This table provides a macro-level lens for the regional convergence story.

---

## Key Relationships for Analysis

| Analysis | Tables Joined | Join Keys |
|---|---|---|
| Regional convergence scatter plot | Table 1 (2015 vs 2023) | `Region`, `Year` |
| Caraga province deep-dive | Table 1, Table 11, Table 12 | `Region = CARAGA`, `Province`, `Year` |
| Butuan City trend | Table 1a | `HUC = Butuan City`, `Year` |
| Poverty depth vs. incidence | Table 1 + Table 11 | `Region`, `Province`, `Year` |
| Island group comparison | Table 13 | `Island_Group`, `Year` |

---

## Known Data Quality Flags

| Flag | Description | How to handle |
|---|---|---|
| CV > 20% | Estimate is statistically unreliable | Exclude from rankings; use cluster groupings |
| CPI base year break | 2015 uses 2006-based CPI; 2018+ uses 2012-based | Compare incidence rates only, not peso thresholds |
| BARMM/Sulu 2021 revision | Figures revised post-release due to food price corrections | Always use latest portal download |
| Missing 2023 magnitude | Tables 5 & 6 not yet updated on OpenSTAT for 2023 | Use PDF publication for 2023 magnitude figures |

---

*Philippine Regional Poverty Divergence Tracker*
*24-Week Data Analytics Foundations Program — Froncoyz Verano*
