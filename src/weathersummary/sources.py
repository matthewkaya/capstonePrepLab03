import requests

from .models import WeatherRecord


class WeatherSource:
    """Downloads weather data and creates weather records."""

    def __init__(self, url, timeout=10):
        self.url = url
        self.timeout = timeout

    def fetch_records(self):
        try:
            response = requests.get(self.url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException:
            print("Unable to download weather data.")
            return []

        try:
            times = data["hourly"]["time"]
            temperatures = data["hourly"]["temperature_2m"]
            precipitation = data["hourly"]["precipitation"]
        except (KeyError, TypeError):
            print("Weather data is missing required hourly fields.")
            return []

        if (
            len(times) != len(temperatures)
            or len(times) != len(precipitation)
        ):
            print("Weather data lists have different lengths.")
            return []

        records = []

        for time, temperature, rain in zip(
            times, temperatures, precipitation
        ):
            if not isinstance(time, str):
                continue

            record = WeatherRecord(
                time,
                temperature,
                rain
            )

            records.append(record)

        return records