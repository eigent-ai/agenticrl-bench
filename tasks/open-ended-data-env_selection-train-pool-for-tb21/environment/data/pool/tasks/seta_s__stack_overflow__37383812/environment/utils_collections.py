"""Data collection utility functions for grouping and counting."""


def group_by(items, key_fn):
    """Group a list of items by the result of key_fn applied to each item."""
    groups = {}
    for item in items:
        key = key_fn(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    return groups


def frequency_count(items):
    """Count the frequency of each unique item in a list."""
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1]))
