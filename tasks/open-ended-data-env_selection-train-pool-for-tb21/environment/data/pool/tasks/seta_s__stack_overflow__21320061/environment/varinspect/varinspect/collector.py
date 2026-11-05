"""Collector module for merging variable captures from multiple functions.

Aggregates captured variables from different analysis stages into a
single unified report dictionary.
"""

import json
import os


def load_config():
    """Load the configuration file.

    Returns:
        dict: Configuration settings.
    """
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
    with open(config_path) as f:
        return json.load(f)


def filter_by_type(variables, exclude_types):
    """Remove variables whose type name is in the exclusion list.

    Args:
        variables: dict of variable name -> value
        exclude_types: list of type name strings to exclude

    Returns:
        dict: Filtered variables.
    """
    filtered = {}
    for name, value in variables.items():
        type_name = type(value).__name__
        if type_name not in exclude_types:
            filtered[name] = value
    return filtered


def merge_captures(existing, new_capture):
    """Merge a new capture into the existing collection.

    Args:
        existing: The current accumulated captures dict.
        new_capture: The new capture dict to merge in.

    Returns:
        dict: The merged result.
    """
    existing = new_capture
    return existing
