from src.quarantine.air_quality import AirQualityQuarantine


def test_quarantine_stores_invalid_record():
    quarantine = AirQualityQuarantine()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 999,
        "longitude": 13.2,
        "pm10": -5,
        "pm2_5": 10,
        "carbon_monoxide": 200,
    }

    errors = [
        "Invalid latitude",
        "Invalid pm10",
    ]

    quarantine.add(record, errors)

    assert quarantine.records == [
        {
            "record": record,
            "errors": errors,
        }
    ]


def test_quarantine_stores_multiple_invalid_records():
    quarantine = AirQualityQuarantine()

    record_1 = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 999,
        "longitude": 13.2,
        "pm10": -5,
        "pm2_5": 10,
        "carbon_monoxide": 200,
    }

    errors_1 = [
        "Invalid latitude",
        "Invalid pm10",
    ]

    record_2 = {
        "timestamp": "2026-08-01T01:00",
        "latitude": 10.0,
        "longitude": 20.0,
        "pm10": -10,
        "pm2_5": -2,
        "carbon_monoxide": 100,
    }

    errors_2 = [
        "Invalid pm10",
        "Invalid pm2_5",
    ]

    quarantine.add(record_1, errors_1)
    quarantine.add(record_2, errors_2)

    assert quarantine.records == [
        {
            "record": record_1,
            "errors": errors_1,
        },
        {
            "record": record_2,
            "errors": errors_2,
        },
    ]


def test_quarantine_persists_records_to_jsonl(tmp_path):
    quarantine = AirQualityQuarantine()

    record = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 999,
        "longitude": 13.2,
        "pm10": -5,
        "pm2_5": 10,
        "carbon_monoxide": 200,
    }

    errors = [
        "Invalid latitude",
        "Invalid pm10",
    ]

    quarantine.add(record, errors)

    output_file = tmp_path / "quarantine.jsonl"

    quarantine.save(output_file)

    assert output_file.exists()

    lines = output_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1

    import json

    saved_record = json.loads(lines[0])

    assert saved_record == {
        "record": record,
        "errors": errors,
    }


def test_quarantine_persists_multiple_records_to_jsonl(tmp_path):
    quarantine = AirQualityQuarantine()

    record_1 = {
        "timestamp": "2026-08-01T00:00",
        "latitude": 999,
        "longitude": 13.2,
        "pm10": -5,
        "pm2_5": 10,
        "carbon_monoxide": 200,
    }

    errors_1 = [
        "Invalid latitude",
        "Invalid pm10",
    ]

    record_2 = {
        "timestamp": "2026-08-01T01:00",
        "latitude": 10.0,
        "longitude": 20.0,
        "pm10": -10,
        "pm2_5": -2,
        "carbon_monoxide": 100,
    }

    errors_2 = [
        "Invalid pm10",
        "Invalid pm2_5",
    ]

    quarantine.add(record_1, errors_1)
    quarantine.add(record_2, errors_2)

    output_file = tmp_path / "quarantine.jsonl"

    quarantine.save(output_file)

    lines = output_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 2

    import json

    assert json.loads(lines[0]) == {
        "record": record_1,
        "errors": errors_1,
    }

    assert json.loads(lines[1]) == {
        "record": record_2,
        "errors": errors_2,
    }