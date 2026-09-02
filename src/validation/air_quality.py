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

        latitude = record.get("latitude")

        if latitude is None or not (-90 <= latitude <= 90):
            return {
                "valid": False,
                "reason": "Invalid latitude",
            }

        return {
            "valid": True,
            "reason": None,
        }
