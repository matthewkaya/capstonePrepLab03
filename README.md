# AIGC5005 Lab 03

This project is the updated version of my Lab 02 weather program. In this lab I changed the program to use classes and a Python package structure.

## Data Source

Weather data comes from the Open-Meteo API. I am using Toronto weather data for the past 7 days.

## Setup

Create and activate the conda environment.

```bash
conda env create -f environment.yml
conda activate weathersummary
```

Install the requirements and the package.

```bash
pip install -r requirements.txt
pip install -e .
```

## Run

```bash
python main.py
```

The result will be saved in `data/processed/summary.json`.

## Test

```bash
python -m unittest discover -s tests
```

The tests work offline and do not need the weather API.

## Layout

The main files are:

```text
main.py
src/weathersummary/
    config.py
    models.py
    sources.py
    aggregations.py
    report.py
tests/
    test_models.py
data/
    raw/
    processed/
```

## What moved where

| Lab 02 | Lab 03 |
|---|---|
| `fetch_records()` | `WeatherSource.fetch_records()` |
| `build_hourly_records()` | `WeatherSource` and `WeatherRecord` |
| `group_temperatures_by_day()` | `TemperatureAggregation.compute()` |
| `calculate_daily_temperature_summary()` | `TemperatureAggregation.compute()` |
| `calculate_daily_precipitation()` | `PrecipitationAggregation.compute()` |
| `find_warmest_day()` | `WarmestDayAggregation.compute()` |
| `get_unique_dates()` | `build_summary()` |
| `build_summary()` | `report.py` |
| `write_summary()` | `report.py` |
| `main()` | `main.py` |
| configuration values | `config.py` |

## Design choices

I used `WeatherRecord` for one hourly weather record and `WeatherSource` for getting the data from the API.

I used an `Aggregation` base class. The temperature, precipitation and warmest day classes inherit from it and have their own `compute()` method. A new aggregation can be added by making another class that inherits from `Aggregation`.

## Known limitations

The program needs an internet connection to download the weather data.

It is currently setup for Toronto and processes the past 7 days of data.