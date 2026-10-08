import unittest

from weathersummary.models import WeatherRecord


class TestWeatherRecord(unittest.TestCase):

    def test_valid_weather_record(self):
        record = WeatherRecord(
            "2026-10-08T12:00",
            20.5,
            0.2
        )

        self.assertEqual(record.time, "2026-10-08T12:00")
        self.assertEqual(record.temperature, 20.5)
        self.assertEqual(record.precipitation, 0.2)

    def test_invalid_weather_values(self):
        record = WeatherRecord(
            "2026-10-08T12:00",
            "invalid",
            "invalid"
        )

        self.assertIsNone(record.temperature)
        self.assertIsNone(record.precipitation)


if __name__ == "__main__":
    unittest.main()