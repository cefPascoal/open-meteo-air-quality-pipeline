from datetime import date
from typing import Any

from src.api.open_meteo import OpenMeteoClient
from src.config import LocationConfig


class AirQualityIngestion:
    def __init__(self, client: OpenMeteoClient) -> None:
        self.client = client

    def fetch(
        self,
        location: LocationConfig,
        start_date: date,
        end_date: date,
        variables: tuple[str, ...],
    ) -> dict[str, Any]:
        data = self.client.fetch_air_quality(
            location=location,
            start_date=start_date,
            end_date=end_date,
            variables=variables,
        )

        return {
            "location": location.name,
            "country": location.country,
            "data": data,
        }

    def fetch_many(
        self,
        locations: list[LocationConfig],
        start_date: date,
        end_date: date,
        variables: tuple[str, ...],
    ) -> list[dict[str, Any]]:
        results = []

        for location in locations:
            result = self.fetch(
                location=location,
                start_date=start_date,
                end_date=end_date,
                variables=variables,
            )
            results.append(result)

        return results