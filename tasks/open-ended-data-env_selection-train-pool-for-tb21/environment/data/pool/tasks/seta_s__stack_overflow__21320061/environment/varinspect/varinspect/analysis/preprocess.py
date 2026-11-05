"""Stage 1: Data preprocessing.

Loads raw data, cleans it, and prepares it for computation.
Creates lists, dicts, scalars, and named tuple records.
"""

from collections import namedtuple
from varinspect.capture import capture_variables

DataRecord = namedtuple("DataRecord", ["id", "value", "label"])


def preprocess():
    """Run the preprocessing stage.

    Returns:
        dict: Captured variables from this stage.
    """
    raw_data = [
        {"id": 1, "value": 23.5, "label": "alpha"},
        {"id": 2, "value": 47.1, "label": "beta"},
        {"id": 3, "value": 12.8, "label": "gamma"},
        {"id": 4, "value": 55.3, "label": "delta"},
        {"id": 5, "value": 31.0, "label": "epsilon"},
    ]

    cleaned = [r for r in raw_data if r["value"] > 15.0]
    record_count = len(cleaned)

    records = [DataRecord(id=r["id"], value=r["value"], label=r["label"]) for r in cleaned]

    mean_value = sum(r["value"] for r in cleaned) / record_count
    labels = [r["label"] for r in cleaned]

    stage_info = {
        "stage": "preprocess",
        "input_count": len(raw_data),
        "output_count": record_count,
        "mean_value": round(mean_value, 2),
    }

    return capture_variables(tag="preprocess")
