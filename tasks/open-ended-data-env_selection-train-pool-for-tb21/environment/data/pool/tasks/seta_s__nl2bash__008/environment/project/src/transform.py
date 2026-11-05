"""Data transformation module for the processing pipeline."""


def normalize_record(record):
    """Return a copy of record with string values stripped of whitespace."""
    return {k: v.strip() if isinstance(v, str) else v for k, v in record.items()}


def filter_nulls(records):
    """Remove records that contain any None value."""
    return [r for r in records if all(v is not None for v in r.values())]


def apply_schema(records, required_keys):
    """Keep only records that have all required keys."""
    return [r for r in records if all(k in r for k in required_keys)]
