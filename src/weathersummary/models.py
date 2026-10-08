class WeatherRecord:
    """Represents one hourly weather record."""

    def __init__(self, time, temperature, precipitation):
        self.time = time

        if isinstance(temperature, (int, float)):
            self.temperature = temperature
        else:
            self.temperature = None

        if isinstance(precipitation, (int, float)):
            self.precipitation = precipitation
        else:
            self.precipitation = None

    def __str__(self):
        return (
            f"{self.time}: {self.temperature} C, "
            f"{self.precipitation} mm"
        )