from src.orchestration.air_quality import AirQualityOrchestrator


class FakeValidator:
    def __init__(self, valid=True, errors=None):
        self.valid = valid
        self.errors = errors or []

    def validate(self, record):
        return {
            "valid": self.valid,
            "errors": self.errors,
        }


class FakeOutput:
    def __init__(self):
        self.records = []

    def write(self, record):
        self.records.append(record)


class FakeQuarantine:
    def __init__(self):
        self.records = []

    def add(self, record, errors):
        self.records.append({
            "record": record,
            "errors": errors,
        })


def test_valid_record_is_sent_to_output():
    record = {
        "timestamp": "2026-01-01T12:00:00",
        "latitude": -8.8383,
        "longitude": 13.2344,
        "pm10": 10.0,
        "pm2_5": 5.0,
        "carbon_monoxide": 200.0,
    }

    validator = FakeValidator()
    output = FakeOutput()
    quarantine = FakeQuarantine()

    orchestrator = AirQualityOrchestrator(
        validator=validator,
        output=output,
        quarantine=quarantine,
    )

    orchestrator.process([record])

    assert output.records == [record]
    assert quarantine.records == []


def test_invalid_record_is_sent_to_quarantine():
    record = {
        "timestamp": "2026-01-01T12:00:00",
        "latitude": -8.8383,
        "longitude": 13.2344,
        "pm10": -10.0,
        "pm2_5": 5.0,
        "carbon_monoxide": 200.0,
    }

    validator = FakeValidator(
        valid=False,
        errors=["Invalid pm10"],
    )

    output = FakeOutput()
    quarantine = FakeQuarantine()

    orchestrator = AirQualityOrchestrator(
        validator=validator,
        output=output,
        quarantine=quarantine,
    )

    orchestrator.process([record])

    assert output.records == []
    assert quarantine.records == [{
        "record": record,
        "errors": ["Invalid pm10"],
    }]


def test_multiple_records_are_routed_correctly():
    records = [
        {
            "timestamp": "2026-01-01T12:00:00",
            "latitude": -8.8383,
            "longitude": 13.2344,
            "pm10": 10.0,
            "pm2_5": 5.0,
            "carbon_monoxide": 200.0,
        },
        {
            "timestamp": "2026-01-01T13:00:00",
            "latitude": -8.8383,
            "longitude": 13.2344,
            "pm10": -10.0,
            "pm2_5": 5.0,
            "carbon_monoxide": 200.0,
        },
        {
            "timestamp": "2026-01-01T14:00:00",
            "latitude": -8.8383,
            "longitude": 13.2344,
            "pm10": 20.0,
            "pm2_5": 8.0,
            "carbon_monoxide": 300.0,
        },
    ]

    class MultipleRecordsValidator:
        def validate(self, record):
            if record["pm10"] < 0:
                return {
                    "valid": False,
                    "errors": ["Invalid pm10"],
                }

            return {
                "valid": True,
                "errors": [],
            }

    validator = MultipleRecordsValidator()
    output = FakeOutput()
    quarantine = FakeQuarantine()

    orchestrator = AirQualityOrchestrator(
        validator=validator,
        output=output,
        quarantine=quarantine,
    )

    orchestrator.process(records)

    assert output.records == [
        records[0],
        records[2],
    ]

    assert quarantine.records == [
        {
            "record": records[1],
            "errors": ["Invalid pm10"],
        }
    ]