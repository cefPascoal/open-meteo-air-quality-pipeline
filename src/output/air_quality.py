import json
from pathlib import Path
from typing import Any


class AirQualityOutput:
    def __init__(self, output_file: Path) -> None:
        self.output_file = output_file

    def write(self, record: dict[str, Any]) -> None:
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        with self.output_file.open("a", encoding="utf-8") as file:
            file.write(json.dumps(record) + "\n")