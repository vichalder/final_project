# AGENTS.md — AI Agent Context & Hand-off

This file is the single source of truth for AI agents working in this repo. Read it before starting any task. Update the **Hand-off notes** section before ending a session.

---

## Project snapshot

**What:** DTU group project — a COVID-19 data story website comparing pandemic response strategies across countries.

**Goal:** Publish an interactive, narrative-driven website (GitHub Pages) that tells a data story: which government interventions correlated with better epidemiological outcomes?

**Stack:**
- Analysis: Python · pandas · plotly · folium · matplotlib
- Website: HTML · CSS (glassmorphism, pastel palette) · vanilla JS
- Deployment: GitHub Pages (source: `/pages/`)

**Team:** Victor, Katarina, Julie

---

## Repo map

```
data/
  epidemiology.csv               # Raw: 12.5M rows, daily cases/deaths/tests per location
  oxford-government-response.csv # Raw: 304K rows, policy stringency + measures
  merged_covid_data.csv          # CANONICAL INPUT for all analysis (170K rows × 30 cols)
  countries.geojson              # Boundaries for choropleth maps

notebooks/
  Data_cleaning_and_merging.ipynb  # Produces merged_covid_data.csv — run first
  Kats_arbejdsfil.ipynb            # Main analysis: spread + stringency visualizations
  victors_workfile.ipynb           # Folium interactive choropleth maps
  Julies_arbejdsfil.ipynb          # In progress / empty
  data_viewer.ipynb                # Utility: lists all location keys → keys.csv

plots/                             # Exported interactive HTML visualizations
  global_spread.html               # Folium choropleth (13.9MB)
  total_deaths_world.html          # Plotly deaths trend
  total_infections_world.html      # Plotly infections trend

pages/
  index.html                       # Homepage — the only deployed file so far
```

**Key files to read before working on the website:** `pages/index.html`

**Key files to read before working on analysis:** `notebooks/Data_cleaning_and_merging.ipynb`, `notebooks/Kats_arbejdsfil.ipynb`

---

## Design conventions

- **Color system:** CSS custom properties defined at the top of `pages/index.html` (`:root`). Always use these variables — never hardcode colors.
  - `--pastel-blue`, `--pastel-purple`, `--pastel-pink`, `--pastel-mint`
  - `--glass-bg`: `rgba(255,255,255,0.25)` · `--glass-border`: `rgba(255,255,255,0.45)`
  - `--text-dark` / `--text-mid` / `--text-light`
- **Glassmorphism pattern:** `background: var(--glass-bg)` + `backdrop-filter: blur(14px)` + `border: 1px solid var(--glass-border)` + `border-radius: 20–24px`
- **Typography:** `Playfair Display` (headings) · `Inter` (body)
- **Comments:** Only write a comment when the WHY is non-obvious. No descriptive comments.

---

## Current state

| Area | Status |
|---|---|
| Data pipeline (clean + merge) | Done |
| Analysis notebooks (Kat, Victor) | In progress |
| Static visualizations (PNG) | Done |
| Interactive plots (HTML) | Done — not yet embedded in website |
| Homepage (`pages/index.html`) | Done — structure + design, placeholder content |
| Three.js globe in hero | Not started (placeholder div exists) |
| "The Story" section with real content | Not started |
| GitHub Pages configuration | Not done |
| Julie's notebook | Not started |

---

## Task board

- [ ] Replace globe placeholder in `pages/index.html` with Three.js animated globe + floating particles
- [ ] Build out "The Story" section with real narrative content and embedded visualizations from `/plots/`
- [ ] Wire `plots/global_spread.html`, `total_deaths_world.html`, `total_infections_world.html` into the website (iframes or inline)
- [ ] Configure GitHub Pages: set source to `/pages/` directory in repo settings
- [ ] Complete `notebooks/Julies_arbejdsfil.ipynb`
- [ ] Remove unrelated Danish data files: `cykeltaellinger_2017.csv`, `trafiktaelling.csv`, `skoler.csv`, `statens_data.csv`

---

## Hand-off notes

_Update this section before ending each session. Include: what you did, what you left unfinished, and any decisions made._

**2026-04-18 — Victor (human) + Claude:**
- Created `pages/index.html`: glassmorphism homepage with nav, hero (globe placeholder), stats strip, story card grid, footer
- Created `README.md` and `AGENTS.md`
- Globe in hero is a styled `<div class="globe-placeholder">` with a float animation — ready to be replaced with Three.js
- Design system (CSS variables, fonts, card pattern) is established in `index.html` — follow it for all future pages
