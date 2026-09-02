from datetime import datetime
from typing import Any


class AirQualityValidator:
    def validate(self, record: dict[str, Any]) -> dict[str, Any]:
        try:
            datetime.fromisoformat(record["timestamp"])
        except (ValueError, TypeError, KeyError):
            return {
                "valid": False,
                "reason": "Invalid timestamp",
            }

        return {
            "valid": True,
            "reason": None,
        }
