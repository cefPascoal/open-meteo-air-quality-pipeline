from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class LocationConfig:
    name: str
    country: str
    latitude: float
    longitude: float
    timezone: str


@dataclass(frozen=True)
class PeriodConfig:
    start_date: date
    end_date: date


@dataclass(frozen=True)
class SourceConfig:
    name: str
    base_url: str


@dataclass(frozen=True)
class PipelineSettings:
    name: str
    version: int


@dataclass(frozen=True)
class PipelineConfig:
    pipeline: PipelineSettings
    source: SourceConfig
    period: PeriodConfig
    variables: tuple[str, ...]
    locations: tuple[LocationConfig, ...]

import os
from pathlib import Path

import yaml

def load_yaml(path: Path)-> dict:
    with path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Estrutura YAML invalida: {path}")

    return data

def load_config(
    pipeline_path: Path,
    locations_path: Path,
) -> PipelineConfig:
    pipeline_data = load_yaml(pipeline_path)
    locations_data = load_yaml(locations_path)

    pipeline = pipeline_data["pipeline"]
    source = pipeline_data["source"]
    period = pipeline_data["period"]

    locations = tuple(
        LocationConfig(
            name=location["name"],
            country=location["country"],
            latitude=float(location["latitude"]),
            longitude=float(location["longitude"]),
            timezone=location["timezone"],
        )
        for location in locations_data["locations"]
    )

    return PipelineConfig(
        pipeline=PipelineSettings(
            name=pipeline["name"],
            version=int(pipeline["version"]),
        ),
        source=SourceConfig(
            name=source["name"],
            base_url=os.path.expandvars(source["base_url"]),
        ),
        period=PeriodConfig(
            start_date=date.fromisoformat(period["start_date"]),
            end_date=date.fromisoformat(period["end_date"]),
        ),
        variables=tuple(pipeline_data["variables"]),
        locations=locations,
    )

def validate_config(config: PipelineConfig) -> None:
    if not config.source.base_url:
        raise ValueError("API base URL cannot be empty.")

    if not config.variables:
        raise ValueError("At least one air quality variable is required.")

    if config.period.start_date > config.period.end_date:
        raise ValueError("Start date cannot be after end date.")

    if not config.locations:
        raise ValueError("At least one location is required.")

    for location in config.locations:
        if not -90 <= location.latitude <= 90:
            raise ValueError(
                f"Invalid latitude for {location.name}: {location.latitude}"
            )

        if not -180 <= location.longitude <= 180:
            raise ValueError(
                f"Invalid longitude for {location.name}: {location.longitude}"
            )

        if not location.timezone:
            raise ValueError(
                f"Timezone cannot be empty for {location.name}."
            )