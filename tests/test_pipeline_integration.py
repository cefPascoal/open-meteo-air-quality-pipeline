import json
from datetime import date

from src.config import LocationConfig
from src.ingestion.air_quality import AirQualityIngestion
from src.orchestration.air_quality import AirQualityOrchestrator
from src.output.air_quality import AirQualityOutput
from src.quarantine.air_quality import AirQualityQuarantine
from src.transformation.air_quality import AirQualityTransformation
from src.validation.air_quality import AirQualityValidator


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
            "timezone": "Africa/Luanda",
            "hourly": {
                "time": [
                    "2026-01-01T12:00:00",
                    "2026-01-01T13:00:00",
                ],
                "pm10": [
                    10.0,
                    -10.0,
                ],
                "pm2_5": [
                    5.0,
                    5.0,
                ],
                "carbon_monoxide": [
                    200.0,
                    200.0,
                ],
            },
        }


def test_pipeline_integrates_ingestion_transformation_and_orchestration(
    tmp_path,
):
    location = LocationConfig(
        name="Luanda",
        country="Angola",
        latitude=-8.8383,
        longitude=13.2344,
        timezone="Africa/Luanda",
    )

    output_file = tmp_path / "output" / "air_quality.jsonl"

    ingestion = AirQualityIngestion(FakeOpenMeteoClient())
    transformation = AirQualityTransformation()
    validator = AirQualityValidator()
    output = AirQualityOutput(output_file)
    quarantine = AirQualityQuarantine()

    ingestion_result = ingestion.fetch(
        location=location,
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 1),
        variables=(
            "pm10",
            "pm2_5",
            "carbon_monoxide",
        ),
    )

    records = transformation.transform(ingestion_result)

    orchestrator = AirQualityOrchestrator(
        validator=validator,
        output=output,
        quarantine=quarantine,
    )

    orchestrator.process(records)

    lines = output_file.read_text(encoding="utf-8").splitlines()

    assert [json.loads(line) for line in lines] == [
        records[0],
    ]

    assert quarantine.records == [
        {
            "record": records[1],
            "errors": ["Invalid pm10"],
        }
    ]