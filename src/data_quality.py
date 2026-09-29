import json
from pathlib import Path


def get_output_locations(output_file: Path) -> set[str]:
    locations = set()

    with output_file.open("r", encoding="utf-8") as file:
        for line in file:
            record = json.loads(line)
            locations.add(record["location"])

    return locations


def get_missing_locations(
    output_file: Path,
    expected_locations: set[str],
) -> set[str]:
    actual_locations = get_output_locations(output_file)

    return expected_locations - actual_locations