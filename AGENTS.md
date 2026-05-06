# AGENTS.md — AI Agent Context & Hand-off

This file is the single source of truth for AI agents working in this repo. Read it before starting any task. Update the **Hand-off notes** section before ending a session.

---

## Project snapshot

**What:** DTU group project — a COVID-19 data story website comparing pandemic response strategies across countries.

**Goal:** Publish an interactive, narrative-driven single-page website (GitHub Pages) that tells a scrolling data story: which government interventions correlated with better epidemiological outcomes?

**Stack:**
- Analysis: Python · pandas · plotly · folium · matplotlib
- Website: HTML · CSS (glassmorphism, pastel palette) · vanilla JS · Three.js (CDN)
- Deployment: GitHub Pages (source: `/docs/` branch `main`)

**Team:** Victor, Katarina, Julie

---

## Repo map

```
data/
  epidemiology.csv                                    # Raw: ~12.5M rows, daily cases/deaths/tests per location (Google Open Data)
  oxford-government-response.csv                      # Raw: 304K rows, policy stringency + 19 measures (Oxford BSG)
  merged_covid_data.csv                               # CANONICAL INPUT — 2,757 rows × 30 cols; DK/DE/UK only, 2020-01-02 to 2022-07-08
  vaccinations.csv                                    # 157 MB, vaccine dose/person counts with brand breakdowns
  daily-tests-per-thousand-people-smoothed-7-day.csv  # 4.5 MB, OWID testing rates (different schema: Entity/Code/Day columns)
  epidemiologi_global_covid_data.csv                  # 11 MB, float64 variant of epidemiology.csv — origin unclear, verify before use
  countries.geojson                                   # 14.6 MB — country boundaries, not used by website
  countries-110m.json                                 # 106 KB — TopoJSON, not used (globe fetches from CDN)
  cykeltaellinger_2017.csv                            # UNRELATED — Danish bicycle counts (delete)
  trafiktaelling.csv                                  # UNRELATED — Danish traffic counts (delete)
  skoler.csv                                          # UNRELATED — Danish schools data (delete)
  statens_data.csv                                    # UNRELATED — Danish government data (delete)
  owid-co2-data.csv                                   # OUT OF SCOPE — CO₂ emissions (delete)

notebooks/
  Data_cleaning_and_merging.ipynb  # Produces merged_covid_data.csv — run first; significantly updated 2026-05-06
  Kats_arbejdsfil.ipynb            # Main analysis: all spread + policy + stringency visualizations; outputs go to docs/plots/kats plots/
  victors_workfile.ipynb           # Folium interactive choropleth maps (global_spread.html, fatality_rate_map.html)
  victor_V2.ipynb                  # Produces docs/plots/country_policy_explorer_v2.html — interactive global explorer (186 countries, searchable chip picker, dual-axis)
  Julies_arbejdsfil.ipynb          # Partially started — markdown structure + some code cells (global spread + fatality rate map topics)
  Explainer_Notebook.ipynb         # Done — data-story explainer (motivation, basic stats, data genre metadata)
  data_viewer.ipynb                # Utility: lists all location keys → keys.csv
  Exploring_data.ipynb             # Active — significantly expanded 2026-05-06 (data cleaning exploration, ~1200 new lines)
  ProbablyTrash.ipynb              # Experimental scratchpad — candidate for deletion
  co2_exploration.ipynb            # OUT OF SCOPE — CO₂ analysis (delete)
  generate_fatality_map.py         # Script: generates fatality_rate_map.html via Folium
  keys.csv                         # Reference: all location keys
  input_images/viz1.png            # Input reference image for notebooks

docs/                              # GitHub Pages root — ONLY files here are served
  index.html                       # The entire website (single scroll, one file)
  countries-110m.json              # No longer needed — TopoJSON fetched from CDN (delete)
  utilities/
    structure.md                   # Website section blueprint (planning doc)
  plots/
    global_spread.html                              # Folium choropleth — embedded in Section 1
    confirmed_cases.png                             # 7-day avg new cases DK/DE/UK — embedded in Section 2 (copied from kats plots/)
    global_new_confirmed_cases_updated.png          # Updated global confirmed cases PNG (Kat, 2026-05-06)
    country_policy_explorer_v2.html                 # Interactive global explorer — embedded in Section 5; produced by victor_V2.ipynb
    total_infections_world.html                     # Plotly infections trend (not currently embedded)
    total_deaths_world.html                         # Plotly deaths trend (not currently embedded)
    fatality_rate_map.html                          # Folium fatality rate choropleth (not currently embedded)
    dashboard.html                                  # Cases/deaths/vaccination/stringency dashboard — embedded in Section 4
    testing_chart.html                              # Testing rates DK/DE/UK — embedded in Section 4
    testing_map.html                                # Global testing map — embedded in Section 4
    testing_map_chart.html                          # Combined testing map + chart (not currently embedded)
    testing_policy.html                             # Testing policy timeline (not currently embedded)
    stay_at_home.html                               # Stay-at-home requirements — embedded in Section 3 grid
    workplace_closing.html                          # Workplace closure — embedded in Section 3 grid
    school_closing.html                             # School closure — embedded in Section 3 grid
    public_transport_closing.html                   # Public transport closure — embedded in Section 3 grid
    facial_coverings.html                           # Facial coverings policy (not currently embedded)
    vaccination_policy.html                         # Vaccination policy timeline (not currently embedded)
    world_map_total_confirmed_infections_latest.html
    world_map_total_covid_deaths_latest.html
    kats plots/                    # Kat's PNG and interactive HTML exports (35+ files)
      confirmed_cases.png          # 7-day avg new cases for DK/DE/UK (original; root-level copy is what index.html uses)
      interactive_government_stringency_index_7day_avg.html  # Embedded in Section 1 continued
      interactive_daily_new_confirmed_cases_per_100k_7day_avg.html
      interactive_country_group_policy_explorer.html
      interactive_bar_chart_cumulative_cases_and_deaths_per_100k.html
      animated_world_monthly_new_confirmed_cases.html
      # ... and 30+ additional PNGs (policy correlations, small multiples, etc.)
```

**Key file for all website work:** `docs/index.html`

**Key files for analysis work:** `notebooks/Data_cleaning_and_merging.ipynb`, `notebooks/Kats_arbejdsfil.ipynb`, `notebooks/victor_V2.ipynb`

**Important:** Notebook outputs (HTML/PNG) are saved into `notebooks/` first, then copied into `docs/plots/` or `docs/plots/kats plots/` — only files inside `docs/` are accessible on GitHub Pages.

---

## Dataset schemas

### `data/merged_covid_data.csv` — CANONICAL INPUT

Shape: **2,757 rows × 30 cols** · Countries: **DK, DE, UK** · Date range: 2020-01-02 to 2022-07-08

All numeric columns are float64.

| Column group | Columns |
|---|---|
| Keys | `date`, `location_key` |
| Epidemiology | `new_confirmed`, `new_deceased`, `new_recovered`, `new_tested`, `cumulative_confirmed`, `cumulative_deceased`, `cumulative_recovered`, `cumulative_tested` |
| Policy measures | `school_closing`, `workplace_closing`, `cancel_public_events`, `restrictions_on_gatherings`, `public_transport_closing`, `stay_at_home_requirements`, `restrictions_on_internal_movement`, `international_travel_controls`, `income_support`, `debt_relief`, `fiscal_measures`, `international_support`, `public_information_campaigns`, `testing_policy`, `contact_tracing`, `emergency_investment_in_healthcare`, `investment_in_vaccines`, `facial_coverings`, `vaccination_policy` |
| Summary | `stringency_index` |

### `data/epidemiology.csv` — RAW source (~12.5M rows)

Columns: `date`, `location_key`, `new_confirmed` (int64), `new_deceased` (int64), `new_recovered` (float64), `new_tested` (float64), `cumulative_confirmed` (int64), `cumulative_deceased` (int64), `cumulative_recovered` (float64), `cumulative_tested` (float64)

### `data/oxford-government-response.csv` — RAW source (304K rows)

Columns: `date`, `location_key`, all 19 policy measure columns (int64, same names as in merged file), `stringency_index` (float64)

### `data/vaccinations.csv` — (157 MB)

Columns: `date`, `location_key`, then 30 float64 vaccination metrics. Includes totals plus per-brand breakdowns for **Pfizer, Moderna, Janssen, Sinovac**. Each brand has: `new_persons_vaccinated_*`, `cumulative_persons_vaccinated_*`, `new_persons_fully_vaccinated_*`, `cumulative_persons_fully_vaccinated_*`, `new_vaccine_doses_administered_*`, `cumulative_vaccine_doses_administered_*`.

### `data/daily-tests-per-thousand-people-smoothed-7-day.csv` — (4.5 MB, OWID)

**Different schema from all other files.** Columns: `Entity` (country name), `Code` (ISO code), `Day` (date string), `Daily tests per thousand people (7-day smoothed)` (float64), `Daily tests per thousand people (7-day smoothed) (Annotations)` (float64)

### `data/epidemiologi_global_covid_data.csv` — (11 MB)

Same columns as `epidemiology.csv` but all numeric columns are float64 instead of int64. Appears to be a pre-cleaned variant. Relationship to `epidemiology.csv` is unclear — verify before using.

---

## Design conventions

- **Theme:** Supports light and dark mode via `[data-theme]` on `<html>`. Default follows system `prefers-color-scheme`, persisted in `localStorage`.
- **Color system:** CSS custom properties in `:root` and `[data-theme="dark"]` at top of `docs/index.html`. Always use variables — never hardcode colors.
  - `--pastel-blue`, `--pastel-purple`, `--pastel-pink`, `--pastel-mint`
  - `--glass-bg` · `--glass-border` · `--body-bg` · `--blob-opacity` · `--blob-blur`
  - `--text-dark` / `--text-mid` / `--text-light`
- **Glassmorphism pattern:** `background: var(--glass-bg)` + `backdrop-filter: blur(14px)` + `border: 1px solid var(--glass-border)` + `border-radius: 20–24px`
- **Typography:** `Playfair Display` (headings) · `Inter` (body, 300–600)
- **Background:** 5 animated morphing blobs (`position: fixed`, `z-index: -1`) — pure CSS, no JS
- **Globe:** Three.js in a `<script type="module">`, country borders from `https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json` via `topojson-client` UMD global. Interactive drag to rotate.
- **Story layout:** Long-form narrative — `.chapter` (prose column, max 680px) followed by `.viz-wrap` (full-width iframe, max 1100px). No cards. Tall iframes use `.viz-wrap-tall`.
- **Dark mode + iframes:** The dark mode toggle broadcasts `postMessage({ covidTheme: theme }, '*')` to all embedded iframes so Plotly charts can respond to theme changes.
- **Comments:** Only write a comment when the WHY is non-obvious.

---

## Current state

| Area | Status |
|---|---|
| Data pipeline (clean + merge) | Done |
| Analysis notebooks (Kat, Victor) | Done — all visualizations exported |
| Static visualizations (PNG) | Done — 35+ PNGs in `docs/plots/kats plots/` |
| Interactive plots (HTML) | Done — 14+ HTML files in `docs/plots/` |
| Three.js globe with real country borders | Done |
| Animated morphing blob background | Done |
| Dark mode toggle (with iframe postMessage) | Done |
| Section 1: A Virus Goes Global + stringency | Done |
| Section 2: Focus countries (DK/DE/UK) + testing context | Done |
| Section 3: The Age of Lockdown (4-panel restriction grid) | Done |
| Section 4: Interventions — Testing + Vaccination | Done |
| Section 5: The Question That Remains (interactive) | Done |
| Explainer notebook | Done |
| GitHub Pages configuration | Done (`/docs/`, branch `main`) |
| Julie's notebook | Partially started — markdown structure + some code, no outputs yet |
| Conclusions / key findings footer | Not started |
| Cleanup: remove unrelated data + out-of-scope notebooks | Not done |

---

## Task board

- [x] Add Section 2: focus countries (DK/DE/UK)
- [x] Add Section 3: Age of Lockdown — 4-panel restriction grid
- [x] Add Section 4: Testing + Vaccination interventions
- [x] Add Section 5: Interactive exploration / "The Question That Remains"
- [ ] Add conclusions / key findings section at the bottom of the page
- [ ] Complete `notebooks/Julies_arbejdsfil.ipynb` (partially started)
- [ ] Remove unrelated data files: `cykeltaellinger_2017.csv`, `trafiktaelling.csv`, `skoler.csv`, `statens_data.csv`, `owid-co2-data.csv`
- [ ] Remove out-of-scope notebooks: `co2_exploration.ipynb`, `ProbablyTrash.ipynb`
- [ ] Remove `docs/countries-110m.json` (TopoJSON is now fetched from CDN)

---

## Hand-off notes

_Update this section before ending each session. Include: what you did, what you left unfinished, and any decisions made._

**2026-04-18 — Victor (human) + Claude:**
- Built `docs/index.html` from scratch: glassmorphism design, pastel palette, Inter + Playfair Display fonts
- Hero: Three.js globe with real country borders (TopoJSON via jsDelivr CDN + topojson-client UMD), 90 floating pastel particles, mouse/touch drag
- Background: 5 animated CSS morphing blobs (`position: fixed`) — pure CSS, no JS cost
- Story section: replaced card grid with long-form narrative layout (`.chapter` prose + `.viz-wrap` iframes)
- Chapter 1 live: narrative text + `global_spread.html` embedded as iframe (`loading="lazy"`)
- Dark mode: `[data-theme]` on `<html>`, toggle button in nav, persists to `localStorage`, defaults to system preference
- GitHub Pages: configured to serve from `/docs/` — live at `https://vichalder.github.io/final_project/`
- Globe fetches TopoJSON from CDN (not local file) — works on GitHub Pages and local servers; does NOT work with `file://` (fetch is blocked on file:// by all browsers — this is expected)
- Plots must be copied into `docs/plots/` to be accessible on GitHub Pages

**2026-04-21 — Victor (human) + Claude:**
- Styled `docs/plots/global_spread.html` to match `index.html`: injected Inter font, `#ede8f5` body background, glassmorphism on the time slider, zoom controls, legend, and attribution bar — all via a CSS block appended to `<head>` (file is Folium-generated so editing JS/data was avoided)
- Added Chapter 2 to `docs/index.html`: prose introducing Denmark, Germany, and UK as focus countries; embeds `docs/plots/kats plots/confirmed_cases.png` in a `.viz-wrap` card

**2026-05-03 — Victor (human) + Claude:**
- Audited entire codebase; rewrote AGENTS.md to reflect actual state
- Corrections: top-level `plots/` folder never existed; `merged_covid_data.csv` has 2,757 rows (DK/DE/UK only), not 170K; website is fully built out across 5 sections, not "Chapters 3+ not started"
- Found previously undocumented: `docs/plots/kats plots/` (35+ files from Kats_arbejdsfil.ipynb), `docs/utilities/structure.md`, notebooks `Explainer_Notebook.ipynb`, `Exploring_data.ipynb`, `ProbablyTrash.ipynb`, `co2_exploration.ipynb`, `generate_fatality_map.py`
- Added dataset schemas section covering all data files including column names and dtypes

**2026-05-04 to 2026-05-06 — Victor + Katarina + Julie (team):**
- Victor: created `notebooks/victor_V2.ipynb` — produces `docs/plots/country_policy_explorer_v2.html`, a fully interactive standalone chart using the raw `epidemiology.csv` (186 countries), with searchable chip country picker (max 3), dual-axis parameter selection, and solid/dashed line encoding. This is now embedded in Section 5 of `index.html`.
- Victor: fixed styling/responsiveness on several section 3 policy plots (`stay_at_home.html`, `workplace_closing.html`, `school_closing.html`, `public_transport_closing.html`); refreshed `global_spread.html` CSS
- Victor: copied `docs/plots/kats plots/confirmed_cases.png` to `docs/plots/confirmed_cases.png` so Section 2 embed path is at root of `plots/` (avoids URL-encoding issues with the space in "kats plots")
- Katarina: updated `Kats_arbejdsfil.ipynb`; added `docs/plots/global_new_confirmed_cases_updated.png`
- Julie: significantly expanded `Data_cleaning_and_merging.ipynb` and `Exploring_data.ipynb` (~2000 new lines total); `Julies_arbejdsfil.ipynb` now has markdown structure + partial code but no exported outputs yet
