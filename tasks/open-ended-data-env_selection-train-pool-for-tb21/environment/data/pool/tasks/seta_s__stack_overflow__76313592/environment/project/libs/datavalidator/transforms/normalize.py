def normalize_record(record):
    """Normalize a validated record."""
    normalized = dict(record)

    if 'name' in normalized:
        normalized['name'] = normalized['name'].strip().title()

    if 'email' in normalized:
        normalized['email'] = normalized['email'].strip().lower()

    if 'tags' in normalized and not isinstance(normalized['tags'], list):
        normalized['tags'] = [normalized['tags']]

    return normalized


def batch_normalize(records):
    """Normalize a batch of records."""
    return [normalize_record(r) for r in records]
