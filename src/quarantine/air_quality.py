import json

from pathlib import Path
from typing import Any


class AirQualityQuarantine:
    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def add(
        self,
        record: dict[str, Any],
        errors: list[str],
    ) -> None:
        self.records.append({
            "record": record,
            "errors": errors,
        })

    def save(self, output_file: Path) -> None:
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with output_file.open("w", encoding="utf-8") as file:
            for record in self.records:
                file.write(json.dumps(record) + "\n")