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

        longitude = record.get("longitude")

        if longitude is None or not (-180 <= longitude <= 180):
            return {
                    "valid": False,
                    "reason": "Invalid longitude",
            }
        pm10 = record.get("pm10")

        if pm10 is None or pm10 < 0:
            return {
                "valid": False,
                "reason": "Invalid pm10",
            }
        
        return {
            "valid": True,
            "reason": None,
        }
