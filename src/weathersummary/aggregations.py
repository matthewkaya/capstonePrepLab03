class Aggregation:
    """Base class for weather aggregations."""

    def compute(self, records):
        raise NotImplementedError


class TemperatureAggregation(Aggregation):
    """Calculates daily temperature statistics."""

    def compute(self, records):
        daily_temperatures = {}

        for record in records:
            date = record.time.split("T")[0]
            temperature = record.temperature

            if temperature is None:
                continue

            if date not in daily_temperatures:
                daily_temperatures[date] = []

            daily_temperatures[date].append(temperature)

        summary = {}

        for date, temperatures in daily_temperatures.items():
            summary[date] = {
                "min_temperature": min(temperatures),
                "max_temperature": max(temperatures),
                "mean_temperature": round(
                    sum(temperatures) / len(temperatures), 2
                )
            }

        return summary
    
class PrecipitationAggregation(Aggregation):
    """Calculates total precipitation for each day."""

    def compute(self, records):
        daily_precipitation = {}

        for record in records:
            date = record.time.split("T")[0]
            precipitation = record.precipitation

            if precipitation is None:
                continue

            daily_precipitation[date] = (
                daily_precipitation.get(date, 0) + precipitation
            )

        return daily_precipitation    

class WarmestDayAggregation(Aggregation):
    """Finds the day with the highest maximum temperature."""

    def compute(self, records):
        daily_max_temperatures = {}

        for record in records:
            date = record.time.split("T")[0]
            temperature = record.temperature

            if temperature is None:
                continue

            if (
                date not in daily_max_temperatures
                or temperature > daily_max_temperatures[date]
            ):
                daily_max_temperatures[date] = temperature

        warmest_day = max(
            daily_max_temperatures,
            key=daily_max_temperatures.get
        )

        return {
            "date": warmest_day,
            "temperature": daily_max_temperatures[warmest_day]
        }    