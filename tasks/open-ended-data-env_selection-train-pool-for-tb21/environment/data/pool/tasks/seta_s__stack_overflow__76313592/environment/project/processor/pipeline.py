import json
from processor.utils import load_config, transform_record
from datavalidator import Validator


class Pipeline:
    def __init__(self, config=None):
        self.config = config or load_config()
        self.validator = Validator()

    def process(self, input_data):
        results = []
        for record in input_data:
            validated = self.validator.validate(record)
            transformed = transform_record(validated)
            results.append(transformed)
        return results

    def get_pipeline_info(self):
        return {"name": "DataProcessor", "version": "1.0"}
