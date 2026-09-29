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