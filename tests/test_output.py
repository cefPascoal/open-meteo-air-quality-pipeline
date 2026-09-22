import json

from src.output.air_quality import AirQualityOutput


def test_output_writes_record_to_jsonl(tmp_path):
    output_file = tmp_path / "air_quality.jsonl"

    record = {
        "timestamp": "2026-01-01T12:00:00",
        "latitude": -8.8383,
        "longitude": 13.2344,
        "pm10": 10.0,
        "pm2_5": 5.0,
        "carbon_monoxide": 200.0,
    }

    output = AirQualityOutput(output_file)

    output.write(record)

    lines = output_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 1
    assert json.loads(lines[0]) == record


def test_output_appends_multiple_records(tmp_path):
    output_file = tmp_path / "air_quality.jsonl"

    records = [
        {
            "timestamp": "2026-01-01T12:00:00",
            "latitude": -8.8383,
            "longitude": 13.2344,
            "pm10": 10.0,
            "pm2_5": 5.0,
            "carbon_monoxide": 200.0,
        },
        {
            "timestamp": "2026-01-01T13:00:00",
            "latitude": -8.8383,
            "longitude": 13.2344,
            "pm10": 20.0,
            "pm2_5": 8.0,
            "carbon_monoxide": 300.0,
        },
    ]

    output = AirQualityOutput(output_file)

    for record in records:
        output.write(record)

    lines = output_file.read_text(encoding="utf-8").splitlines()

    assert len(lines) == 2
    assert [json.loads(line) for line in lines] == records


def test_output_creates_parent_directory(tmp_path):
    output_file = tmp_path / "output" / "air_quality.jsonl"

    record = {
        "timestamp": "2026-01-01T12:00:00",
        "latitude": -8.8383,
        "longitude": 13.2344,
        "pm10": 10.0,
        "pm2_5": 5.0,
        "carbon_monoxide": 200.0,
    }

    output = AirQualityOutput(output_file)

    output.write(record)

    assert output_file.exists()