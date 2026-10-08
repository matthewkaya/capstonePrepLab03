import json
from pathlib import Path

import requests

SOURCE_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=43.65"
    "&longitude=-79.38"
    "&hourly=temperature_2m,precipitation"
    "&past_days=7"
    "&forecast_days=0"
    "&timezone=America/Toronto"
)

OUTPUT = Path("summary.json")


def fetch_records(url):
    """Download weather data from the API and return it as Python data."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print("Unable to download weather data.")
        return None


def build_hourly_records(data):
    """Combine hourly weather lists into a list of weather records."""

    try:
        times = data["hourly"]["time"]
        temperatures = data["hourly"]["temperature_2m"]
        precipitation = data["hourly"]["precipitation"]
    except (KeyError, TypeError):
        print("Weather data is missing required hourly fields.")
        return None

    if (
        len(times) != len(temperatures)
        or len(times) != len(precipitation)
    ):
        print("Weather data lists have different lengths.")
        return None

    records = []

    for time, temperature, rain in zip(
        times, temperatures, precipitation
    ):
        if not isinstance(time, str):
            continue

        if temperature is not None and not isinstance(
            temperature, (int, float)
        ):
            continue

        if rain is not None and not isinstance(
            rain, (int, float)
        ):
            continue

        record = {
            "time": time,
            "temperature": temperature,
            "precipitation": rain
        }

        records.append(record)

    return records

def group_temperatures_by_day(records):
    """Group temperature values by date."""
    daily_temperatures = {}

    for record in records:
        date = record["time"].split("T")[0]
        temperature = record["temperature"]

        if temperature is None:
            continue

        if date not in daily_temperatures:
            daily_temperatures[date] = []

        daily_temperatures[date].append(temperature)

    return daily_temperatures

def calculate_daily_temperature_summary(daily_temperatures):
    """Calculate minimum, maximum, and mean temperature for each day."""
    summary = {}

    for date, temperatures in daily_temperatures.items():
        summary[date] = {
            "min_temperature": min(temperatures),
            "max_temperature": max(temperatures),
            "mean_temperature": round(sum(temperatures) / len(temperatures), 2)
        }

    return summary

def calculate_daily_precipitation(records):
    """Calculate total precipitation for each day."""
    daily_precipitation = {}

    for record in records:
        date = record["time"].split("T")[0]
        precipitation = record["precipitation"]

        if precipitation is None:
            continue

        daily_precipitation[date] = (
            daily_precipitation.get(date, 0) + precipitation
        )

    return daily_precipitation

def find_warmest_day(temperature_summary):
    """Return the day with the highest maximum temperature."""
    max_temperatures = {
        date: values["max_temperature"]
        for date, values in temperature_summary.items()
    }

    warmest_day = max(max_temperatures, key=max_temperatures.get)

    return {
        "date": warmest_day,
        "temperature": max_temperatures[warmest_day]
    }  

def get_unique_dates(records):
    """Return the unique dates found in the weather records."""
    unique_dates = set()

    for record in records:
        date = record["time"].split("T")[0]
        unique_dates.add(date)

    return unique_dates

def build_summary(records):
    """Build the final weather summary dictionary."""
    daily_temperatures = group_temperatures_by_day(records)
    temperature_summary = calculate_daily_temperature_summary(
        daily_temperatures
    )
    daily_precipitation = calculate_daily_precipitation(records)
    warmest_day = find_warmest_day(temperature_summary)
    unique_dates = get_unique_dates(records)

    summary = {
        "source_url": SOURCE_URL,
        "records_processed": len(records),
        "unique_days": len(unique_dates),
        "daily_temperature_summary": temperature_summary,
        "daily_precipitation": daily_precipitation,
        "warmest_day": warmest_day
    }

    return summary

def write_summary(summary, path):
    """Write the summary dictionary to a JSON file."""
    with path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

def main():
    data = fetch_records(SOURCE_URL)

    if data is None:
        return

    records = build_hourly_records(data)

    if records is None or len(records) == 0:
        print("No valid weather records to process.")
        return

    summary = build_summary(records)

    write_summary(summary, OUTPUT)
    print("Weather summary written to summary.json.")


if __name__ == "__main__":
    main()
    