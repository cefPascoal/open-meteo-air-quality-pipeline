class AirQualityQuarantine:
    def __init__(self):
        self.records = []

    def add(self, record, errors):
        self.records.append({
            "record": record,
            "errors": errors,
        })