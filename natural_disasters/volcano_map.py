import csv
from pathlib import Path

import plotly.express as px

path = Path("natural_disasters/data/volcanos.csv")
lines = path.read_text().splitlines()
reader = csv.reader(lines, delimiter=";")
header_row = next(reader)
data_rows = list(reader)

dates, veis, lons, lats, names, countries = [], [], [], [], [], []
for row in data_rows:
    coords = row[12].split(", ")
    dates.append(row[0])
    lats.append(float(coords[0]))
    lons.append(float(coords[1]))
    veis.append(float(row[9]) if row[9] else 0)
    names.append(row[2])
    countries.append(row[1])


fig = px.scatter_geo(
    lat=lats,
    lon=lons,
    size=veis,
    title="Global Volcanic Eruptions 1000-2020",
    color=veis,
    color_continuous_scale="reds",
    labels={"color": "Volcanic Explosivity Index"},
    projection="natural earth",
    hover_name=names,
    hover_data={"date": dates, "country": countries},
)

fig.update_traces(marker=dict(line=dict(width=1, color="black")))

fig.show()
