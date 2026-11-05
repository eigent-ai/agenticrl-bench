from datavalidator.schemas import InputSchema
from datavalidator.transforms import normalize_record


class Validator:
    def __init__(self):
        self._schema = InputSchema

    def validate(self, data):
        if isinstance(data, dict):
            schema = self._schema(**data)
            normalized = normalize_record(schema.dict())
            return normalized
        raise ValueError(f"Expected dict, got {type(data)}")

    def __repr__(self):
        return f"<Validator schema={self._schema.__name__}>"
