import json

from .aggregations import (
    TemperatureAggregation,
    PrecipitationAggregation,
    WarmestDayAggregation
)


def build_summary(records, source_url):
    """Build the final weather summary dictionary."""

    aggregations = [
        ("daily_temperature_summary", TemperatureAggregation()),
        ("daily_precipitation", PrecipitationAggregation()),
        ("warmest_day", WarmestDayAggregation())
    ]

    summary = {
        "source_url": source_url,
        "records_processed": len(records),
        "unique_days": len({
            record.time.split("T")[0]
            for record in records
        })
    }

    for name, aggregation in aggregations:
        summary[name] = aggregation.compute(records)

    return summary


def write_summary(summary, path):
    """Write the summary dictionary to a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)