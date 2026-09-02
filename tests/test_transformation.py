import pytest

from src.transformation.air_quality import AirQualityTransformation


def test_transform_hourly_data_to_records():
    ingestion_result = {
        "location": "Beijing",
        "country": "China",
        "data": {
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "hourly": {
                "time": [
                    "2026-01-01T00:00",
                    "2026-01-01T01:00",
                ],
                "pm10": [12.5, 13.1],
            },
        },
    }

    transformation = AirQualityTransformation()

    result = transformation.transform(ingestion_result)

    assert result == [
        {
            "location": "Beijing",
            "country": "China",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "timestamp": "2026-01-01T00:00",
            "pm10": 12.5,
        },
        {
            "location": "Beijing",
            "country": "China",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "timestamp": "2026-01-01T01:00",
            "pm10": 13.1,
        },
    ]

def test_transform_multiple_hourly_variables():
    ingestion_result = {
        "location": "Beijing",
        "country": "China",
        "data": {
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "hourly": {
                "time": [
                    "2026-01-01T00:00",
                    "2026-01-01T01:00",
                ],
                "pm10": [12.5, 13.1],
                "pm2_5": [8.2, 9.4],
            },
        },
    }

    transformation = AirQualityTransformation()

    result = transformation.transform(ingestion_result)

    assert result == [
        {
            "location": "Beijing",
            "country": "China",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "timestamp": "2026-01-01T00:00",
            "pm10": 12.5,
            "pm2_5": 8.2,
        },
        {
            "location": "Beijing",
            "country": "China",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "timestamp": "2026-01-01T01:00",
            "pm10": 13.1,
            "pm2_5": 9.4,
        },
    ]



from src.transformation.air_quality import AirQualityTransformation


def test_transform_raises_error_when_variable_length_differs_from_timestamps():
    ingestion_result = {
        "location": "Beijing",
        "country": "China",
        "data": {
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "hourly": {
                "time": [
                    "2026-01-01T00:00",
                    "2026-01-01T01:00",
                ],
                "pm10": [12.5],
            },
        },
    }

    transformation = AirQualityTransformation()

    with pytest.raises(ValueError, match="Variable 'pm10' has 1 values but 2 timestamps"):
        transformation.transform(ingestion_result)

def test_transform_raises_error_when_no_hourly_variables_are_present():
    ingestion_result = {
        "location": "Beijing",
        "country": "China",
        "data": {
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "hourly": {
                "time": [
                    "2026-01-01T00:00",
                    "2026-01-01T01:00",
                ],
            },
        },
    }

    transformation = AirQualityTransformation()

    with pytest.raises(
        ValueError,
        match="No hourly air quality variables were provided",
    ):
        transformation.transform(ingestion_result)

def test_transform_raises_error_when_time_is_missing():
    ingestion_result = {
        "location": "Beijing",
        "country": "China",
        "data": {
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "hourly": {
                "pm10": [12.5, 13.1],
            },
        },
    }

    transformation = AirQualityTransformation()

    with pytest.raises(
        ValueError,
        match="Hourly data must contain 'time'",
    ):
        transformation.transform(ingestion_result)

def test_transform_preserves_none_values():
    ingestion_result = {
        "location": "Beijing",
        "country": "China",
        "data": {
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "hourly": {
                "time": [
                    "2026-01-01T00:00",
                    "2026-01-01T01:00",
                ],
                "pm10": [12.5, None],
            },
        },
    }

    transformation = AirQualityTransformation()

    result = transformation.transform(ingestion_result)

    assert result == [
        {
            "location": "Beijing",
            "country": "China",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "timestamp": "2026-01-01T00:00",
            "pm10": 12.5,
        },
        {
            "location": "Beijing",
            "country": "China",
            "latitude": 39.9042,
            "longitude": 116.4074,
            "timezone": "Asia/Shanghai",
            "timestamp": "2026-01-01T01:00",
            "pm10": None,
        },
    ]