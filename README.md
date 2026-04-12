# Housing Data Analysis

This project analyzes housing-related data based on three datasets from Leipzig's open data portal. The goal is to explore household composition, housing costs, and living conditions over time.

---

## Data Sources

The analysis is based on three dataframes:

---

### 1. `df_size` — Household Size (`haushaltsgruesse.json`)

**Years sampled:**  
2010, 2015–2023

**Categories per year:**

- **Households**
  - 1 person
  - 2 persons
  - 3 persons
  - 4+ persons
  - Total (sum of subcategories)
- **Average household size**

---

### 2. `df_type` — Household Type (`haushaltstyp.json`)

**Years sampled:**  
2018–2023

**Data cleaning note:**

For the years **2018, 2020, and 2022**, data for *"Alleinerziehende"* (single parents) is missing (only *"Alleinstehende < 65 J."* is present).  
Since this affects **50% of the samples**, all *"Alleinerziehende"* rows were removed from the analysis.

**Categories per year:**

- **Average total rent burden by household type**
  - Retired couples
  - Single retirees
  - Couples without children
  - Couples with children
  - Single (< 65 years)
- **Average total rent burden (overall)**

---

### 3. `df_situation` — Housing Situation (`wohnsituation.json`)

**Years sampled:**  
2000–2004 (missing 2004), 2005–2024

**Categories per year:**

#### Average living space per person (sqm)
- Total
- 1-person households
- 2-person households
- 3-person households
- 4+ person households
- Age groups:
  - 18–34
  - 35–54
  - 55+
- Household types:
  - Singles
  - Single retirees
  - Single parents
  - Couples with children
  - Couples without children
  - Retired couples

#### Average number of rooms per person
- Same categories as above

#### Housing status (% share)
- Rented apartment or house
- Owner-occupied apartment
- Own house
- Other

---

## Data Cleaning

- All duplicated and non-relevant columns were removed
- Each dataset was reduced from ~16 columns to **4–5 meaningful columns**
- Missing or inconsistent categories were handled as described above

---

## Notes

- All datasets are structured as time series with categorical breakdowns
- Some categories are incomplete across years and were excluded when necessary
- Units were normalized (e.g., `m²` → `sqm`)

---

## Author

Manuel Quintana