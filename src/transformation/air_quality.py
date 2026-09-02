from typing import Any


class AirQualityTransformation:
    def transform(self, ingestion_result: dict[str, Any]) -> list[dict[str, Any]]:
        location = ingestion_result["location"]
        country = ingestion_result["country"]

        data = ingestion_result["data"]

        latitude = data["latitude"]
        longitude = data["longitude"]
        timezone = data["timezone"]

        hourly = data["hourly"]

        if "time" not in hourly:
            raise ValueError("Hourly data must contain 'time'")

        times = hourly["time"]

        variables = {
            key: values
            for key, values in hourly.items()
            if key != "time"
        }

        if not variables:
            raise ValueError("No hourly air quality variables were provided")

        for variable_name, values in variables.items():
            if len(values) != len(times):
                raise ValueError(
                    f"Variable '{variable_name}' has {len(values)} values "
                    f"but {len(times)} timestamps"
                )

        records = []

        for index, timestamp in enumerate(times):
            record = {
                "location": location,
                "country": country,
                "latitude": latitude,
                "longitude": longitude,
                "timezone": timezone,
                "timestamp": timestamp,
            }

            for variable_name, values in variables.items():
                record[variable_name] = values[index]

            records.append(record)

        return records