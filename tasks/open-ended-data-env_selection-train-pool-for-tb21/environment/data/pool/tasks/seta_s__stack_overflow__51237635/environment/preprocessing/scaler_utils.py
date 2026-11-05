import numpy as np


def numpy_minmax(X):
    """Per-column min-max scaling to [0, 1] range."""
    xmin = X.min()
    xmax = X.max()
    return (X - xmin) / (xmax - xmin)


def numpy_standardize(X, mean, std):
    """Apply z-score standardization with pre-computed parameters."""
    return (X - mean) / std
