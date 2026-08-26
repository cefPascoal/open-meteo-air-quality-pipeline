from datetime import date

from src.config import (
    LocationConfig,
    PeriodConfig,
    PipelineConfig,
    PipelineSettings,
    SourceConfig,
)


def test_location_config():
    location = LocationConfig(
        name="Beijing",
        country="China",
        latitude=39.9042,
        longitude=116.4074,
        timezone="Asia/Shanghai",
    )

    assert location.name == "Beijing"
    assert location.latitude == 39.9042
    assert location.longitude == 116.4074


def test_pipeline_config():
    config = PipelineConfig(
        pipeline=PipelineSettings(
            name="air-quality-ingestion",
            version=1,
        ),
        source=SourceConfig(
            name="open-meteo-air-quality",
            base_url="https://air-quality-api.open-meteo.com/v1/air-quality",
        ),
        period=PeriodConfig(
            start_date=date(2026, 1, 1),
            end_date=date(2026, 6, 30),
        ),
        variables=("pm10", "pm2_5"),
        locations=(),
    )

    assert config.pipeline.name == "air-quality-ingestion"
    assert config.pipeline.version == 1
    assert config.period.start_date < config.period.end_date
    assert "pm10" in config.variables

from pathlib import Path

from src.config import load_yaml

def test_load_yaml():
    path = Path("config/pipeline.yaml")

    data = load_yaml(path)

    assert "pipeline" in data
    assert "source" in data
    assert "period" in data
    assert "variables" in data

from pathlib import Path

from src.config import load_config

def test_load_config():
    config = load_config(
        Path("config/pipeline.yaml"),
        Path("config/locations.yaml"),
    )

    assert config.pipeline.name == "air-quality-ingestion"
    assert config.pipeline.version == 1

    assert config.source.name == "open-meteo-air-quality"

    assert config.period.start_date == date(2026, 1, 1)
    assert config.period.end_date == date(2026, 6, 30)

    assert "pm10" in config.variables
    assert "pm2_5" in config.variables

    assert len(config.locations) == 3

    beijing = next(
        location
        for location in config.locations
        if location.name == "Beijing"
    )

    assert beijing.latitude == 39.9042
    assert beijing.longitude == 116.4074
    assert beijing.timezone == "Asia/Shanghai"

from src.config import validate_config

def test_validate_config():
    config = load_config(
        Path("config/pipeline.yaml"),
        Path("config/locations.yaml"),
    )

    validate_config(config)

import pytest

def test_validate_config_rejects_invalid_latitude():
    config = load_config(
        Path("config/pipeline.yaml"),
        Path("config/locations.yaml"),
    )

    invalid_location = LocationConfig(
        name="Invalid",
        country="Test",
        latitude=95.0,
        longitude=0.0,
        timezone="UTC",
    )

    invalid_config = PipelineConfig(
        pipeline=config.pipeline,
        source=config.source,
        period=config.period,
        variables=config.variables,
        locations=(invalid_location,),
    )

    with pytest.raises(ValueError, match="Invalid latitude"):
        validate_config(invalid_config)