import math


def format_value(value, error):
    """Format a numeric value to a string with decimal places appropriate
    for the given measurement error.
    """
    if error == 0:
        return f"{value:.6f}"

    formatted = f"{value:.6f}"
    return formatted
