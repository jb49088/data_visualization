import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt

path = Path("placeholder/weather_data/death_valley_2021.csv")
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)

# Extract dates and precipitation levels
dates, precipitations = [], []
for row in reader:
    date = datetime.strptime(row[2], "%Y-%m-%d")
    try:
        precipitation = float(row[3])
    except ValueError:
        print(f"Missing data for {date}")
    else:
        dates.append(date)
        precipitations.append(precipitation)

# Plot the precipitation levels
plt.style.use("seaborn-v0_8")
fig, ax = plt.subplots()
ax.plot(dates, precipitations, color="blue")

# Format plot
title = "Daily Precipitation Levels, 2021\nDeath Valley, CA"
ax.set_title(title, fontsize=20)
ax.set_xlabel("", fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel("Precipitation (inches)", fontsize=16)
ax.tick_params(labelsize=16)

plt.show()
