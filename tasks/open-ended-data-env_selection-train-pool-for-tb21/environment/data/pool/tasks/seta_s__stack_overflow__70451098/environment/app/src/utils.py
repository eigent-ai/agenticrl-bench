"""Utility functions for data processing."""

import numpy as np


def normalize_dataset(data):
    """Normalize dataset values to a common scale for comparison.

    Divides all values by the maximum value so that the largest
    value maps to 1.0 (or -1.0 for negative peaks).

    Args:
        data: numpy array of measurement values

    Returns:
        numpy array of normalized values
    """
    data = np.array(data, dtype=float)
    max_val = np.max(data)
    if max_val == 0:
        return data
    return data / max_val
