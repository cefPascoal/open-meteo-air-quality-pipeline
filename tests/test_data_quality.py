import json
from pathlib import Path

from src.data_quality import (
    get_missing_locations,
    get_output_locations,
)


def test_get_output_locations(tmp_path: Path):
    output_file = tmp_path / "air_quality.jsonl"

    records = [
        {"location": "Luanda"},
        {"location": "Lisbon"},
        {"location": "Beijing"},
    ]

    output_file.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )

    locations = get_output_locations(output_file)

    assert locations == {"Luanda", "Lisbon", "Beijing"}


def test_get_missing_locations(tmp_path: Path):
    output_file = tmp_path / "air_quality.jsonl"

    records = [
        {"location": "Luanda"},
        {"location": "Lisbon"},
    ]

    output_file.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )

    expected_locations = {"Luanda", "Lisbon", "Beijing"}

    missing = get_missing_locations(
        output_file,
        expected_locations,
    )

    assert missing == {"Beijing"}


from datetime import datetime


def test_output_timestamps_are_within_configured_period(tmp_path: Path):
    output_file = tmp_path / "air_quality.jsonl"

    records = [
        {"timestamp": "2026-01-01T00:00"},
        {"timestamp": "2026-03-15T12:00"},
        {"timestamp": "2026-06-30T23:00"},
    ]

    output_file.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n",
        encoding="utf-8",
    )

    start_date = datetime.fromisoformat("2026-01-01T00:00")
    end_date = datetime.fromisoformat("2026-06-30T23:59:59")

    timestamps = [
        datetime.fromisoformat(record["timestamp"])
        for record in records
    ]

    assert all(
        start_date <= timestamp <= end_date
        for timestamp in timestamps
    )