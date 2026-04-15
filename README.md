# Leipzig Housing Data Analysis 🏚️

This project analyzes housing-related data based on three datasets from Leipzig's open data portal. The goal is to explore household composition, housing costs, and living conditions over time.

---

## tl;dr (for full analysis and graphics jump to "📊 Insights" section)

- The data reveals a clear shift toward **smaller, more individual households**, combined with **high dependence on renting**.
- Younger and single households are apparently the most **economically constrained**, while older individuals tend to have **more space and rooms per person**.

---

## Data Sources

The analysis is based on three data sources provided by "Open Data-Portal der Stadt Leipzig" (under Datenlizenz Deutschland Namensnennung 2.0), all information retrieved on 12.04.2026:

### 1. `df_size` — Household Size (`haushaltsgruesse.json`)

- data source: [Bautätigkeit und Wohnen / Haushaltsgröße (Jahreszahlen)](https://statistik.leipzig.de/opendata/api/values?kategorie_nr=6&rubrik_nr=23&periode=y&format=json)

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

### 2. `df_type` — Household Type (`haushaltstyp.json`)
- data source: [Bautätigkeit und Wohnen / Gesamtmietbelastung nach Haushaltstyp (Jahreszahlen)](https://statistik.leipzig.de/opendata/api/values?kategorie_nr=6&rubrik_nr=27&periode=y&format=json)

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

### 3. `df_situation` — Housing Situation (`wohnsituation.json`)
- data source:[Bautätigkeit und Wohnen / Wohnsituation (Jahreszahlen)](https://statistik.leipzig.de/opendata/api/values?kategorie_nr=6&rubrik_nr=2&periode=y&format=json)

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

## Data Cleaning

- All duplicated and non-relevant columns were removed
- Each dataset was reduced from ~16 columns to **5 meaningful columns**
- Missing or inconsistent categories were handled as described above
- A cleaned dataset can be found under "datasets/full_cleaned_data.json"

## Notes

- All datasets are structured as time series with categorical breakdowns
- Some categories are incomplete across years and were excluded when necessary
- Units were normalized (e.g., `m²` → `sqm`)

---

# 📊 Insights

## 1. Household Size Evolution
<img src="/generated_plots/1.1%20-%20Household%20size%20evolution%20over%20time.png" width="100%" />

- The average household size shows a steady decline over time.
- This suggests a long-term trend toward smaller households.
- The decrease is gradual but consistent, indicating demographic changes.

---

## 2. Household Size Distribution
<img src="/generated_plots/1.2%20-%20Average%20household%20size%20distribution%20over%20time.png" width="100%" />

- **Single-person households are always increasing** over time.
- Households with 2 or more people are stable.

---

## 3. Housing Cost Burden by Household Type
<img src="/generated_plots/2.1%20-%20Share%20of%20income%20by%20Household%20type%20spent%20on%20housing%20over%20time.png" width="100%" />

- **Single-person households and retirees living alone have the highest housing cost**.
- Couples without children pay always the lowest.

---

## 4. Average Living Space per Person
<img src="/generated_plots/3.1%20-%20Average%20living%20space%20in%20sqm%20per%20person%20by%20household%20composition%20over%20time.png" width="100%" />

- **Living space per person increases with smaller household size**.
- Single-person households have **significantly more space per person than larger households**.
- Over time there is a slight upward trend across all household types.

---

## 5. Rooms per Person by Household Size
<img src="/generated_plots/3.2%20-%20Average%20rooms%20number%20per%20person%20by%20household%20composition%20over%20time.png" width="100%" />

- Smaller households offer more rooms per person than larger households.
- The gap between small and large households remains constant over time.

---

## 6. Rooms per Person by Age Group
<img src="/generated_plots/3.3%20-%20Average%20rooms%20number%20per%20person%20by%20age%20range%20over%20time.png" width="100%" />

- **Older age groups have more rooms per person than younger groups**.
- A **slight increase over time** is visible for older groups, maybe accumulated wealth?

---

## 7. Property Regime Distribution
<img src="/generated_plots/3.4%20-%20Property%20regime%20percentage%20over%20time.png" width="100%" />

- The majority of households are **renting**, with a consistently high percentage (~85%).
- Home ownership (houses and apartments)** remains relatively low and stable.
