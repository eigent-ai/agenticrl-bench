import math


def round_on_error(value, error):
    """Round a value to the precision implied by its measurement error.

    Uses the order of magnitude of the error to determine the rounding
    precision, then rounds the value to that level.
    """
    significant_digits = 10 ** math.floor(math.log(error, 10))
    rounded = value // significant_digits * significant_digits
    return rounded
