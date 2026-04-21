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
  epidemiology.csv               # Raw: 12.5M rows, daily cases/deaths/tests per location
  oxford-government-response.csv # Raw: 304K rows, policy stringency + measures
  merged_covid_data.csv          # CANONICAL INPUT for all analysis (170K rows × 30 cols)
  countries.geojson              # Boundaries for choropleth maps (14.6MB — not used by website)

notebooks/
  Data_cleaning_and_merging.ipynb  # Produces merged_covid_data.csv — run first
  Kats_arbejdsfil.ipynb            # Main analysis: spread + stringency visualizations
  victors_workfile.ipynb           # Folium interactive choropleth maps
  Julies_arbejdsfil.ipynb          # In progress / empty
  data_viewer.ipynb                # Utility: lists all location keys → keys.csv

plots/                             # Source exports — NOT served by GitHub Pages
  global_spread.html               # Folium choropleth (13.9MB)
  total_deaths_world.html          # Plotly deaths trend
  total_infections_world.html      # Plotly infections trend

docs/                              # GitHub Pages root — ONLY files here are served
  index.html                       # The entire website (single scroll, one file)
  plots/
    global_spread.html             # Deployed copy of choropleth — embedded in Chapter 1
    confirmed_cases.png            # 7-day avg new cases for DK/DE/UK — embedded in Chapter 2
```

**Key file for all website work:** `docs/index.html`

**Key files for analysis work:** `notebooks/Data_cleaning_and_merging.ipynb`, `notebooks/Kats_arbejdsfil.ipynb`

**Important:** When adding a new plot to the website, copy it from `plots/` into `docs/plots/` — only files inside `docs/` are accessible on GitHub Pages.

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
- **Story layout:** Long-form narrative — `.chapter` (prose column, max 680px) followed by `.viz-wrap` (full-width iframe, max 1100px). No cards.
- **Comments:** Only write a comment when the WHY is non-obvious.

---

## Current state

| Area | Status |
|---|---|
| Data pipeline (clean + merge) | Done |
| Analysis notebooks (Kat, Victor) | In progress |
| Static visualizations (PNG) | Done |
| Interactive plots (HTML) | Done — `global_spread.html` deployed |
| Three.js globe with real country borders | Done |
| Animated morphing blob background | Done |
| Dark mode toggle | Done |
| Chapter 1 narrative + global spread map | Done |
| Chapter 2 narrative + focus-country cases chart (DK/DE/UK) | Done |
| GitHub Pages configuration | Done (`/docs/`, branch `main`) |
| Chapters 3+ (deaths, stringency, conclusions) | Not started |
| Julie's notebook | Not started |

---

## Task board

- [x] Add Chapter 2: focus countries (DK/DE/UK) — narrative prose + `plots/confirmed_cases.png`
- [ ] Add Chapter 3: total infections over time — embed `plots/total_infections_world.html`
- [ ] Add Chapter 4: deaths — embed `plots/total_deaths_world.html`
- [ ] Add chapters on government stringency and vaccination (pending notebook outputs)
- [ ] Add a conclusions / key findings section at the bottom
- [ ] Complete `notebooks/Julies_arbejdsfil.ipynb`
- [ ] Remove unrelated Danish data files: `cykeltaellinger_2017.csv`, `trafiktaelling.csv`, `skoler.csv`, `statens_data.csv`
- [ ] Remove `docs/countries-110m.json` (no longer needed — TopoJSON now fetched from CDN)

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
- Added Chapter 2 to `docs/index.html`: prose introducing Denmark, Germany, and UK as focus countries; embeds `docs/plots/confirmed_cases.png` in a `.viz-wrap` card
