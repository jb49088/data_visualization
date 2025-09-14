import csv
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


def main(file_name):
    path = Path("weather/data") / file_name

    lines = path.read_text().splitlines()
    reader = csv.reader(lines)
    header_row = next(reader)
    data_rows = list(reader)

    name_index = header_row.index("NAME")
    date_index = header_row.index("DATE")
    precipitation_index = header_row.index("PRCP")

    station_name = data_rows[0][name_index]

    dates, precipitations = _extract_precipitation_data(
        data_rows, date_index, precipitation_index
    )

    _create_visual(dates, precipitations, station_name)


def _extract_precipitation_data(data_rows, date_index, precipitation_index):
    # Extract dates and precipitation levels
    dates, precipitations = [], []
    for row in data_rows:
        date = datetime.strptime(row[date_index], "%Y-%m-%d")
        try:
            precipitation = float(row[precipitation_index])
        except ValueError:
            print(f"Missing data for {date}")
        else:
            dates.append(date)
            precipitations.append(precipitation)

    return dates, precipitations


def _create_visual(dates, precipitations, station_name):
    # Plot the precipitation levels
    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots()
    ax.plot(dates, precipitations, color="blue")

    # Format plot
    title = _create_title(station_name)
    ax.set_title(title, fontsize=20)
    ax.set_xlabel("", fontsize=16)
    fig.autofmt_xdate()
    ax.set_ylabel("Precipitation (inches)", fontsize=16)
    ax.tick_params(labelsize=16)

    plt.show()


def _create_title(station_name):
    if station_name == "SITKA AIRPORT, AK US":
        title = "Daily Precipitation Levels, 2021\nSitka, AK"
    elif station_name == "DEATH VALLEY NATIONAL PARK, CA US":
        title = "Daily Precipitation Levels, 2021\nDeath Valley, CA"

    return title


if __name__ == "__main__":
    sitka = main("sitka_2021.csv")
    death_valley = main("death_valley_2021.csv")
