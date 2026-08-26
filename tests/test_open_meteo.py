import httpx
import pytest

from datetime import date

from src.api.open_meteo import OpenMeteoClient
from src.config import LocationConfig


def test_client_configuration():
    client = OpenMeteoClient(
        base_url="https://air-quality-api.open-meteo.com/v1/air-quality"
    )

    assert client.base_url == (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
    )
    assert client.timeout == 30.0
    assert client.max_retries == 3


def test_fetch_air_quality():
    captured_request = {}

    def mock_transport(request: httpx.Request) -> httpx.Response:
        captured_request["request"] = request

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
        )

        location = LocationConfig(
            name="Beijing",
            country="China",
            latitude=39.9042,
            longitude=116.4074,
            timezone="Asia/Shanghai",
        )

        data = client.fetch_air_quality(
            location=location,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 6, 30),
            variables=("pm10",),
        )

    request = captured_request["request"]

    assert request.url.params["latitude"] == "39.9042"
    assert request.url.params["longitude"] == "116.4074"
    assert request.url.params["hourly"] == "pm10"
    assert request.url.params["start_date"] == "2026-01-01"
    assert request.url.params["end_date"] == "2026-06-30"
    assert request.url.params["timezone"] == "Asia/Shanghai"

    assert data["latitude"] == 39.9042
    assert data["longitude"] == 116.4074
    assert data["hourly"]["pm10"] == [12.5]


def test_fetch_air_quality_raises_on_http_error():
    def mock_transport(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=500,
            json={"error": True},
        )

    transport = httpx.MockTransport(mock_transport)

    with httpx.Client(transport=transport) as http_client:
        client = OpenMeteoClient(
            base_url="https://air-quality-api.open-meteo.com/v1/air-quality",
            http_client=http_client,
        )

        location = LocationConfig(
            name="Beijing",
            country="China",
            latitude=39.9042,
            longitude=116.4074,
            timezone="Asia/Shanghai",
        )

        with pytest.raises(httpx.HTTPStatusError):
            client.fetch_air_quality(
                location=location,
                start_date=date(2026, 1, 1),
                end_date=date(2026, 6, 30),
                variables=("pm10",),
            )


def test_fetch_air_quality_retries_on_server_error():
    responses = [
        httpx.Response(
            status_code=500,
            json={"error": True},
        ),
        httpx.Response(
            status_code=500,
            json={"error": True},
        ),
        httpx.Response(
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
        ),
    ]

    def mock_transport(request: httpx.Request) -> httpx.Response:
        return responses.pop(0)

    transport = httpx.MockTransport(mock_transport)

    with httpx.Client(transport=transport) as http_client:
        client = OpenMeteoClient(
            base_url="https://air-quality-api.open-meteo.com/v1/air-quality",
            max_retries=2,
            http_client=http_client,
        )

        location = LocationConfig(
            name="Beijing",
            country="China",
            latitude=39.9042,
            longitude=116.4074,
            timezone="Asia/Shanghai",
        )

        data = client.fetch_air_quality(
            location=location,
            start_date=date(2026, 1, 1),
            end_date=date(2026, 6, 30),
            variables=("pm10",),
        )

    assert data["hourly"]["pm10"] == [12.5]
    assert responses == []