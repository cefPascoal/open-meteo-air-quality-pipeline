import httpx

from datetime import date

from src.api.open_meteo import OpenMeteoClient
from src.config import LocationConfig
from src.ingestion.air_quality import AirQualityIngestion


def test_ingestion_fetches_data_for_location():
    def mock_transport(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=200,
            json={
                "latitude": 39.9042,
                "longitude": 116.4074,
                "timezone": "Asia/Shanghai",
                "hourly": {
                    "time": ["2026-01-01T00:00"],
                    "pm10": [12.5],
                },
            },
        )

    transport = httpx.MockTransport(mock_transport)

    with httpx.Client(transport=transport) as http_client:
        client = OpenMeteoClient(
            base_url="https://air-quality-api.open-meteo.com/v1/air-quality",
            http_client=http_client,
            sleep_func=lambda _: None,
        )

        ingestion = AirQualityIngestion(client)

        location = LocationConfig(
            name="Beijing",
            country="China",
            latitude=39.9042,
            longitude=116.4074,
            timezone="Asia/Shanghai",
        )

        result = ingestion.fetch(
            location=location,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 6, 30),
            variables=("pm10",),
        )

    assert result["location"] == "Beijing"
    assert result["country"] == "China"
    assert result["data"]["hourly"]["pm10"] == [12.5]


def test_ingestion_fetches_data_for_multiple_locations():
    requests = []

    def mock_transport(request: httpx.Request) -> httpx.Response:
        requests.append(request)

        latitude = float(request.url.params["latitude"])
        longitude = float(request.url.params["longitude"])

        return httpx.Response(
            status_code=200,
            json={
                "latitude": latitude,
                "longitude": longitude,
                "timezone": "UTC",
                "hourly": {
                    "time": ["2026-01-01T00:00"],
                    "pm10": [10.0],
                },
            },
        )

    transport = httpx.MockTransport(mock_transport)

    with httpx.Client(transport=transport) as http_client:
        client = OpenMeteoClient(
            base_url="https://air-quality-api.open-meteo.com/v1/air-quality",
            http_client=http_client,
            sleep_func=lambda _: None,
        )

        ingestion = AirQualityIngestion(client)

        locations = [
            LocationConfig(
                name="Beijing",
                country="China",
                latitude=39.9042,
                longitude=116.4074,
                timezone="Asia/Shanghai",
            ),
            LocationConfig(
                name="Luanda",
                country="Angola",
                latitude=-8.8390,
                longitude=13.2894,
                timezone="Africa/Luanda",
            ),
        ]

        results = ingestion.fetch_many(
            locations=locations,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 2),
            variables=("pm10",),
        )

    assert len(results) == 2

    assert results[0]["location"] == "Beijing"
    assert results[0]["country"] == "China"
    assert results[0]["data"]["latitude"] == 39.9042

    assert results[1]["location"] == "Luanda"
    assert results[1]["country"] == "Angola"
    assert results[1]["data"]["latitude"] == -8.8390

    assert len(requests) == 2
    