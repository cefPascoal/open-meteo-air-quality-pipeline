from src.validation.air_quality import AirQualityValidator


def make_valid_record():
    return {
        "timestamp": "2026-08-01T00:00",
        "latitude": 0.0,
        "longitude": 0.0,
        "pm10": 0.0,
        "pm2_5": 0.0,
        "carbon_monoxide": 0.0,
    }


def test_validate_accepts_valid_record():
    validator = AirQualityValidator()

    result = validator.validate(make_valid_record())

    assert result == {
        "valid": True,
        "errors": [],
    }


# Timestamp


def test_validate_rejects_invalid_timestamp():
    record = make_valid_record()
    record["timestamp"] = "invalid-timestamp"

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid timestamp"],
    }


def test_validate_rejects_none_timestamp():
    record = make_valid_record()
    record["timestamp"] = None

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid timestamp"],
    }


def test_validate_rejects_missing_timestamp():
    record = make_valid_record()
    del record["timestamp"]

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid timestamp"],
    }


# Latitude


def test_validate_rejects_invalid_latitude():
    record = make_valid_record()
    record["latitude"] = 91.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid latitude"],
    }


def test_validate_rejects_latitude_below_minimum():
    record = make_valid_record()
    record["latitude"] = -91.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid latitude"],
    }


def test_validate_accepts_maximum_latitude():
    record = make_valid_record()
    record["latitude"] = 90.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_rejects_none_latitude():
    record = make_valid_record()
    record["latitude"] = None

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid latitude"],
    }


def test_validate_rejects_missing_latitude():
    record = make_valid_record()
    del record["latitude"]

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid latitude"],
    }


# Longitude


def test_validate_rejects_invalid_longitude():
    record = make_valid_record()
    record["longitude"] = 181.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid longitude"],
    }


def test_validate_rejects_longitude_below_minimum():
    record = make_valid_record()
    record["longitude"] = -181.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid longitude"],
    }


def test_validate_accepts_maximum_longitude():
    record = make_valid_record()
    record["longitude"] = 180.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_accepts_minimum_longitude():
    record = make_valid_record()
    record["longitude"] = -180.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_rejects_none_longitude():
    record = make_valid_record()
    record["longitude"] = None

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid longitude"],
    }


def test_validate_rejects_missing_longitude():
    record = make_valid_record()
    del record["longitude"]

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid longitude"],
    }


# PM10


def test_validate_rejects_negative_pm10():
    record = make_valid_record()
    record["pm10"] = -1.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid pm10"],
    }


def test_validate_accepts_zero_pm10():
    record = make_valid_record()
    record["pm10"] = 0.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_accepts_positive_pm10():
    record = make_valid_record()
    record["pm10"] = 12.5

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_rejects_none_pm10():
    record = make_valid_record()
    record["pm10"] = None

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid pm10"],
    }


def test_validate_rejects_missing_pm10():
    record = make_valid_record()
    del record["pm10"]

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid pm10"],
    }


# PM2.5


def test_validate_rejects_negative_pm2_5():
    record = make_valid_record()
    record["pm2_5"] = -1.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid pm2_5"],
    }


def test_validate_accepts_zero_pm2_5():
    record = make_valid_record()
    record["pm2_5"] = 0.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_accepts_positive_pm2_5():
    record = make_valid_record()
    record["pm2_5"] = 12.5

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_rejects_none_pm2_5():
    record = make_valid_record()
    record["pm2_5"] = None

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid pm2_5"],
    }


def test_validate_rejects_missing_pm2_5():
    record = make_valid_record()
    del record["pm2_5"]

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid pm2_5"],
    }


# Carbon monoxide


def test_validate_rejects_negative_carbon_monoxide():
    record = make_valid_record()
    record["carbon_monoxide"] = -1.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid carbon_monoxide"],
    }


def test_validate_accepts_zero_carbon_monoxide():
    record = make_valid_record()
    record["carbon_monoxide"] = 0.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_accepts_positive_carbon_monoxide():
    record = make_valid_record()
    record["carbon_monoxide"] = 150.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": True,
        "errors": [],
    }


def test_validate_rejects_none_carbon_monoxide():
    record = make_valid_record()
    record["carbon_monoxide"] = None

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid carbon_monoxide"],
    }


def test_validate_rejects_missing_carbon_monoxide():
    record = make_valid_record()
    del record["carbon_monoxide"]

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": ["Invalid carbon_monoxide"],
    }


# Validation contract


def test_validate_returns_errors_as_list():
    record = make_valid_record()
    record["pm10"] = -1.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result["valid"] is False
    assert result["errors"] == ["Invalid pm10"]


def test_validate_returns_all_validation_errors():
    record = make_valid_record()

    record["timestamp"] = "invalid-timestamp"
    record["latitude"] = 100.0
    record["longitude"] = 200.0
    record["pm10"] = -1.0
    record["pm2_5"] = -1.0
    record["carbon_monoxide"] = -1.0

    validator = AirQualityValidator()

    result = validator.validate(record)

    assert result == {
        "valid": False,
        "errors": [
            "Invalid timestamp",
            "Invalid latitude",
            "Invalid longitude",
            "Invalid pm10",
            "Invalid pm2_5",
            "Invalid carbon_monoxide",
        ],
    }