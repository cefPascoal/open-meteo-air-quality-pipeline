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
        "pm2_5": 0.0,
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
        "pm2_5": 0.0,
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
        "pm2_5": 0.0,
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
        "pm2_5": 0.0,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid timestamp",
    }


def test_validate_rejects_invalid_latitude():
    record = {
        "location": "Beijing",
        "country": "China",
        "latitude": 91.0,
        "longitude": 116.4074,
        "timezone": "Asia/Shanghai",
        "timestamp": "2026-01-01T00:00",
        "pm10": 12.5,
        "pm2_5": 0.0,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid latitude",
    }


def test_validate_rejects_latitude_below_minimum():
    record = {
        "location": "Beijing",
        "country": "China",
        "latitude": -91.0,
        "longitude": 116.4074,
        "timezone": "Asia/Shanghai",
        "timestamp": "2026-01-01T00:00",
        "pm10": 12.5,
        "pm2_5": 0.0,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid latitude",
    }


def test_validate_accepts_maximum_latitude():
    record = {
        "location": "North Pole",
        "country": "Arctic",
        "latitude": 90.0,
        "longitude": 0.0,
        "timezone": "UTC",
        "timestamp": "2026-01-01T00:00",
        "pm10": 12.5,
        "pm2_5": 0.0,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "reason": None,
    }


def test_validate_rejects_none_latitude():
    record = {
        "location": "Beijing",
        "country": "China",
        "latitude": None,
        "longitude": 116.4074,
        "timezone": "Asia/Shanghai",
        "timestamp": "2026-01-01T00:00",
        "pm10": 12.5,
        "pm2_5": 0.0,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid latitude",
    }


def test_validate_rejects_missing_latitude():
    record = {
        "location": "Beijing",
        "country": "China",
        "longitude": 116.4074,
        "timezone": "Asia/Shanghai",
        "timestamp": "2026-01-01T00:00",
        "pm10": 12.5,
        "pm2_5": 0.0,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid latitude",
    }


def test_validate_rejects_invalid_longitude():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 181.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid longitude",
    }


def test_validate_rejects_longitude_below_minimum():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": -181.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid longitude",
    }


def test_validate_accepts_maximum_longitude():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 180.0,
        "pm10": 0.0,
        "pm2_5": 0.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "reason": None,
    }


def test_validate_accepts_minimum_longitude():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": -180.0,
        "pm10": 0.0,
        "pm2_5": 0.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "reason": None,
    }


def test_validate_rejects_none_longitude():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": None,
    }

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid longitude",
    }


def test_validate_rejects_missing_longitude():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid longitude",
    }


def test_validate_rejects_negative_pm10():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 0.0,
        "pm10": -1.0,
        "pm2_5": 0.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid pm10",
    }


def test_validate_accepts_zero_pm10():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 0.0,
        "pm10": 0.0,
        "pm2_5": 0.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "reason": None,
    }


def test_validate_accepts_positive_pm10():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 0.0,
        "pm10": 12.5,
        "pm2_5": 0.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "reason": None,
    }


def test_validate_rejects_none_pm10():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 0.0,
        "pm10": None,
        "pm2_5": 0.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid pm10",
    }


def test_validate_rejects_missing_pm10():
    validator = AirQualityValidator()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 0.0,
    }

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "reason": "Invalid pm10",
    }


def test_validate_rejects_negative_pm2_5():
    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 0.0,
        "pm10": 0.0,
        "pm2_5": -1.0,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result["valid"] is False
    assert result["reason"] == "Invalid pm2_5"


def test_validate_rejects_none_pm2_5():
    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 0.0,
        "pm10": 0.0,
        "pm2_5": None,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result["valid"] is False
    assert result["reason"] == "Invalid pm2_5"


def test_validate_rejects_missing_pm2_5():
    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 0.0,
        "pm10": 0.0,
    }

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result["valid"] is False
    assert result["reason"] == "Invalid pm2_5"