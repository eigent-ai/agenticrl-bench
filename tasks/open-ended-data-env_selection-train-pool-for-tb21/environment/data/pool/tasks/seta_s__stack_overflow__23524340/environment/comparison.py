import math


def nearly_equal(a, b, sigfig=5):
    """Check if two values are equal to a given number of significant figures.

    Returns True if a and b agree to `sigfig` significant digits.
    """
    if a == 0 or b == 0:
        return abs(a - b) < 0.01

    return abs(a - b) < 10 ** (-sigfig)
