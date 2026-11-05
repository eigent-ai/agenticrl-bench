import numpy as np


def compute_initial_guess(x, y, model_name):
    """Compute initial parameter guesses for curve fitting.

    Parameters are returned in order: (x0, c, k, y0)
    """
    if model_name == "shifted_decay":
        x0 = max(x)
        c = min(y)
        k = 0.01
        y0 = max(y)
        return (x0, c, k, y0)
    else:
        x0 = max(x)
        c = min(y)
        k = 0.01
        y0 = max(y)
        return (x0, c, k, y0)
