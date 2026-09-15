class AirQualityOrchestrator:
    def __init__(self, validator, output, quarantine):
        self.validator = validator
        self.output = output
        self.quarantine = quarantine

    def process(self, records):
        for record in records:
            result = self.validator.validate(record)

            if result["valid"]:
                self.output.write(record)
            else:
                self.quarantine.add(record, result["errors"])