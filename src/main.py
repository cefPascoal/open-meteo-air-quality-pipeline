from pathlib import Path

from src.api.open_meteo import OpenMeteoClient
from src.config import load_config, validate_config
from src.ingestion.air_quality import AirQualityIngestion
from src.transformation.air_quality import AirQualityTransformation
from src.validation.air_quality import AirQualityValidator
from src.quarantine.air_quality import AirQualityQuarantine
from src.output.air_quality import AirQualityOutput
from src.orchestration.air_quality import AirQualityOrchestrator


def run_pipeline(
    pipeline_path: Path,
    locations_path: Path,
    output_dir: Path,
) -> None:
    config = load_config(
        pipeline_path=pipeline_path,
        locations_path=locations_path,
    )

    validate_config(config)

    client = OpenMeteoClient(
        base_url=config.source.base_url,
    )

    ingestion = AirQualityIngestion(client)
    transformation = AirQualityTransformation()
    validator = AirQualityValidator()

    output = AirQualityOutput(
        output_file=output_dir / "air_quality.jsonl",
    )

    quarantine = AirQualityQuarantine()

    orchestrator = AirQualityOrchestrator(
        validator=validator,
        output=output,
        quarantine=quarantine,
    )

    ingestion_results = ingestion.fetch_many(
        locations=list(config.locations),
        start_date=config.period.start_date,
        end_date=config.period.end_date,
        variables=config.variables,
    )

    records = []

    for ingestion_result in ingestion_results:
        records.extend(
            transformation.transform(ingestion_result)
        )

    orchestrator.process(records)

    quarantine.save(
        output_dir / "quarantine.jsonl",
    )


if __name__ == "__main__":
    run_pipeline(
        pipeline_path=Path("config/pipeline.yaml"),
        locations_path=Path("config/locations.yaml"),
        output_dir=Path("data/processed"),
    )