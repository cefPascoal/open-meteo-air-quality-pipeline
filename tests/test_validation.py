from src.validation.air_quality import AirQualityValidator



def test_validate_accepts_valid_timestamp():
    record = {
        "location": "Beijing",
        "country": "China",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "timezone": "Asia/Shanghai",
        "timestamp": "2026-01-01T00:00",
        "pm10": 12.5,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "reason": None,
    }

def test_validate_rejects_invalid_timestamp():
    record = {
        "location": "Beijing",
        "country": "China",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "timezone": "Asia/Shanghai",
        "timestamp": "invalid-timestamp",
        "pm10": 12.5,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid timestamp",
    }

def test_validate_rejects_none_timestamp():
    record = {
        "location": "Beijing",
        "country": "China",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "timezone": "Asia/Shanghai",
        "timestamp": None,
        "pm10": 12.5,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid timestamp",
    }

def test_validate_rejects_missing_timestamp():
    record = {
        "location": "Beijing",
        "country": "China",
        "latitude": 39.9042,
        "longitude": 116.4074,
        "timezone": "Asia/Shanghai",
        "pm10": 12.5,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid timestamp",
    }