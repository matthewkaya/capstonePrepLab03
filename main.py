from weathersummary.config import OUTPUT, SOURCE_URL, TIMEOUT
from weathersummary.report import build_summary, write_summary
from weathersummary.sources import WeatherSource


def main():
    source = WeatherSource(SOURCE_URL, TIMEOUT)
    records = source.fetch_records()

    if len(records) == 0:
        return

    summary = build_summary(records, SOURCE_URL)
    write_summary(summary, OUTPUT)

    print("Weather summary written to data/processed/summary.json.")


if __name__ == "__main__":
    main()