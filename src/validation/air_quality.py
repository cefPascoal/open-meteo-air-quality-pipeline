from datetime import datetime
from typing import Any


class AirQualityValidator:
    def validate(self, record: dict[str, Any]) -> dict[str, Any]:
        try:
            datetime.fromisoformat(record["timestamp"])
        except (ValueError, TypeError, KeyError):
            return {
                "valid": False,
                "errors": ["Invalid timestamp"],
            }

        latitude = record.get("latitude")

        if latitude is None or not (-90 <= latitude <= 90):
            return {
                "valid": False,
                "errors": ["Invalid latitude"],
            }

        longitude = record.get("longitude")

        if longitude is None or not (-180 <= longitude <= 180):
            return {
                "valid": False,
                "errors": ["Invalid longitude"],
            }

        pm10 = record.get("pm10")

        if pm10 is None or pm10 < 0:
            return {
                "valid": False,
                "errors": ["Invalid pm10"],
            }

        pm2_5 = record.get("pm2_5")

        if pm2_5 is None or pm2_5 < 0:
            return {
                "valid": False,
                "errors": ["Invalid pm2_5"],
            }

        carbon_monoxide = record.get("carbon_monoxide")

        if carbon_monoxide is None or carbon_monoxide < 0:
            return {
                "valid": False,
                "errors": ["Invalid carbon_monoxide"],
            }

        return {
            "valid": True,
            "errors": [],
        }
