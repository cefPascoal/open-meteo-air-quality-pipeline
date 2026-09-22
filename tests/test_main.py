from pathlib import Path

from src.main import run_pipeline


class FakeOpenMeteoClient:
    def fetch_air_quality(
        self,
        location,
        start_date,
        end_date,
        variables,
    ):
        return {
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timezone": location.timezone,
            "hourly": {
                "time": ["2026-01-01T00:00"],
                "pm10": [10.0],
                "pm2_5": [5.0],
                "carbon_monoxide": [200.0],
            },
        }


def test_run_pipeline_creates_output_files(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "OPEN_METEO_BASE_URL",
        "https://air-quality-api.open-meteo.com/v1/air-quality",
    )

    monkeypatch.setattr(
        "src.main.OpenMeteoClient",
        lambda base_url: FakeOpenMeteoClient(),
    )

    run_pipeline(
        pipeline_path=Path("config/pipeline.yaml"),
        locations_path=Path("config/locations.yaml"),
        output_dir=tmp_path,
    )

    assert (tmp_path / "air_quality.jsonl").exists()
    assert (tmp_path / "quarantine.jsonl").exists()