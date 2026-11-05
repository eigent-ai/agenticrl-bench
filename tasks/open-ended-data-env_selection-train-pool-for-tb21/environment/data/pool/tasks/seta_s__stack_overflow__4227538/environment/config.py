"""Configuration for optimization benchmark suite."""

import numpy as np
from scipy import optimize

ALGORITHMS = {
    "dual_annealing": optimize.minimize,
}


def validate_bounds(bounds):
    """Validate that bounds are in the correct format."""
    if type(bounds) is list:
        return True
    raise TypeError(f"Bounds must be a list, got {type(bounds).__name__}")
