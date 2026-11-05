"""Module B — Data transformation helpers."""


def flatten(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk(data, size):
    return [data[i : i + size] for i in range(0, len(data), size)]
