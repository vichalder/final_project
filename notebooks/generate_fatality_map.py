"""Generate COVID-19 Monthly Fatality Rate Choropleth Map with Time Slider"""

import json
import math
import pandas as pd
import numpy as np
import folium
from folium.plugins import TimeSliderChoropleth
import branca.colormap as cm
from pathlib import Path

# Load data
current_dir = Path(__file__).parent
data_path = current_dir / "data" / "merged_covid_data.csv"
geojson_path = current_dir / "data" / "countries.geojson"

print("Loading data...")
data = pd.read_csv(data_path)

# 1. Filter to country-level and aggregate by month
country_data = data[
    (data["location_key"].str.len() == 2) &
    (~data["location_key"].str.contains("_"))
].copy()

country_data["date"] = pd.to_datetime(country_data["date"])
country_data["month"] = country_data["date"].dt.to_period("M")

# Aggregate monthly confirmed cases and deaths
monthly = (
    country_data
    .groupby(["location_key", "month"], as_index=False)
    .agg({
        "new_confirmed": "sum",
        "new_deceased": "sum"
    })
)

# Compute monthly fatality rate: (monthly deaths / monthly confirmed) * 100
monthly["fatality_rate"] = np.where(
    monthly["new_confirmed"] > 0,
    (monthly["new_deceased"] / monthly["new_confirmed"]) * 100,
    np.nan
)

monthly["unix_ts"] = monthly["month"].dt.to_timestamp().apply(lambda ts: int(ts.timestamp()))

print(f"Data processed: {len(monthly)} monthly records")
print(f"Fatality rate range: {monthly['fatality_rate'].min():.2f}% - {monthly['fatality_rate'].max():.2f}%")

# 2. Linear colormap for fatality rate
cap_value = float(np.percentile(monthly["fatality_rate"].dropna(), 95))  # 95th percentile

def normalize(val, cap):
    if pd.isna(val) or val < 0:
        return None
    return min(float(val) / cap, 1.0)

colormap = cm.linear.YlOrRd_09.scale(0, 1)
colormap.caption = "Monthly COVID-19 Fatality Rate (%) — Deaths / Confirmed Cases"

# 3. Load GeoJSON and inject top-level id field
NAME_TO_ISO2 = {"France": "FR", "Norway": "NO"}

print("Loading GeoJSON...")
with open(geojson_path, "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

for feature in geojson_data["features"]:
    iso2 = feature["properties"].get("ISO3166-1-Alpha-2", "-99")
    if iso2 == "-99":
        name = feature["properties"].get("name", "")
        iso2 = NAME_TO_ISO2.get(name, "-99")
    feature["id"] = iso2

geojson_str = json.dumps(geojson_data)

# 4. Build styledict: country_id -> {unix_ts_str -> {color, opacity}}
MISSING = {"color": "#d3d3d3", "opacity": 0.4}
DATA_OPACITY = 0.7

all_months = monthly[["month", "unix_ts"]].drop_duplicates().sort_values("month")
monthly_indexed = monthly.set_index(["location_key", "unix_ts"])["fatality_rate"]
geo_countries = {f["id"] for f in geojson_data["features"] if len(f["id"]) == 2}

print(f"Building style dict for {len(geo_countries)} countries and {len(all_months)} months...")

styledict = {}
for cid in geo_countries:
    ts_style = {}
    for _, row in all_months.iterrows():
        ts_str = str(int(row["unix_ts"]))
        try:
            val = monthly_indexed.loc[(cid, int(row["unix_ts"]))]
        except KeyError:
            val = float("nan")
        norm = normalize(val, cap_value)
        ts_style[ts_str] = MISSING if norm is None else {"color": colormap(norm), "opacity": DATA_OPACITY}
    styledict[cid] = ts_style

# 5. Render map
print("Rendering map...")
m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB positron", min_zoom=1, max_bounds=True)
TimeSliderChoropleth(data=geojson_str, styledict=styledict, init_timestamp=0).add_to(m)
colormap.add_to(m)

# Save to both locations
output_path = current_dir / "plots" / "fatality_rate_map.html"
m.save(str(output_path))
print(f"Saved to {output_path}")

docs_output_path = current_dir / "docs" / "plots" / "fatality_rate_map.html"
m.save(str(docs_output_path))
print(f"Saved to {docs_output_path}")

print("Done!")
