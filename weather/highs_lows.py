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
    tmax_index = header_row.index("TMAX")
    tmin_index = header_row.index("TMIN")

    station_name = data_rows[0][name_index]

    dates, highs, lows = _extract_weather_data(
        data_rows, date_index, tmax_index, tmin_index
    )

    _create_visual(dates, highs, lows, station_name)


def _extract_weather_data(data_rows, date_index, tmax_index, tmin_index):
    # Extract dates, and high and low temperatures
    dates, highs, lows = [], [], []
    for row in data_rows:
        date = datetime.strptime(row[date_index], "%Y-%m-%d")
        try:
            high = int(row[tmax_index])
            low = int(row[tmin_index])
        except ValueError:
            print(f"Missing data for {date}")
        else:
            dates.append(date)
            highs.append(high)
            lows.append(low)

    return dates, highs, lows


def _create_visual(dates, highs, lows, station_name):
    # Plot the high and low temperatures
    plt.style.use("seaborn-v0_8")
    fig, ax = plt.subplots()
    ax.plot(dates, highs, color="red", alpha=0.5)
    ax.plot(dates, lows, color="blue", alpha=0.5)
    ax.fill_between(dates, highs, lows, facecolor="blue", alpha=0.1)

    # Format plot with automatic title generation
    title = _create_title(station_name)
    ax.set_title(title, fontsize=20)
    ax.set_xlabel("", fontsize=16)
    fig.autofmt_xdate()
    ax.set_ylabel("Temperature (F)", fontsize=16)
    ax.tick_params(labelsize=16)
    plt.show()


def _create_title(station_name):
    if station_name == "SITKA AIRPORT, AK US":
        title = "Daily High and Low Temperatures, 2021\nSitka, AK"
    elif station_name == "DEATH VALLEY NATIONAL PARK, CA US":
        title = "Daily High and Low Temperatures, 2021\nDeath Valley, CA"

    return title


if __name__ == "__main__":
    sitka = main("sitka_2021.csv")
    death_valley = main("death_valley_2021.csv")
