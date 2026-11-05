def get_results(records):
    results = []
    for record in records:
        if record.get('active'):
            results.append(record)
    return results


def validate_input(data):
    if not isinstance(data, dict):
        raise ValueError("Expected dict")
    return data
