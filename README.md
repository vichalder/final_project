# COVID-19: What approach works for pandemics?

**DTU Data Story · 2026**

A data-driven investigation into how different countries responded to the COVID-19 pandemic — and what the numbers reveal about which strategies actually worked. We compare government response strategies (lockdowns, school closures, travel restrictions, stringency index) against epidemiological outcomes (cases, deaths, excess mortality) across 195 countries.

**Live site:** https://vichalder.github.io/final_project/

---

## Project structure

```
data/
  epidemiology.csv               # Google COVID-19 Open Data — daily cases, deaths, tests (12.5M rows)
  oxford-government-response.csv # Oxford BSG — policy stringency & measures (304K rows)
  merged_covid_data.csv          # Canonical analysis input (output of Data_cleaning_and_merging.ipynb)
  countries.geojson              # Country boundaries for choropleth maps

notebooks/
  Data_cleaning_and_merging.ipynb  # Step 1 — run this first to produce merged_covid_data.csv
  Kats_arbejdsfil.ipynb            # Global spread and government response visualizations
  victors_workfile.ipynb           # Interactive choropleth maps (Folium)
  Julies_arbejdsfil.ipynb          # In progress
  data_viewer.ipynb                # Utility — explore available location keys

plots/
  global_spread.html             # Interactive Folium choropleth map
  total_deaths_world.html        # Plotly global death trends
  total_infections_world.html    # Plotly global infection trends

pages/
  index.html                     # Website homepage (deployed via GitHub Pages)

requirements.txt
```

---

## Data sources

| Dataset | Source |
|---|---|
| `epidemiology.csv` | [Google COVID-19 Open Data](https://health.google.com/covid-19/open-data/) |
| `oxford-government-response.csv` | [Oxford Blavatnik School of Government](https://www.bsg.ox.ac.uk/research/covid-19-government-response-tracker) |

---

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter lab
```

**Notebook run order:**
1. `Data_cleaning_and_merging.ipynb` — produces `data/merged_covid_data.csv`
2. `Kats_arbejdsfil.ipynb` and/or `victors_workfile.ipynb` — analysis and visualizations

---

## Team

- Victor Halder
- Katarina
- Julie
