"""Scientific notation formatting utilities."""

import math
from matplotlib.ticker import ScalarFormatter


class SciNotationFormatter(ScalarFormatter):
    """Custom axis formatter for scientific notation display.

    Provides consistent scientific notation tick labels with configurable
    precision and offset behavior.
    """

    def __init__(self, precision=1, use_offset_config=True, **kwargs):
        super().__init__(**kwargs)
        self.precision = precision
        self.set_useOffset(False)

    def _set_format(self):
        self.format = "%d"

    def format_eng(self, value):
        """Format value to multiplication-style LaTeX notation for text displays."""
        if value == 0:
            return "$0$"

        exponent = int(math.floor(math.log10(abs(value))))
        mantissa = value / (10 ** exponent)

        if mantissa < 0:
            sign = "-"
            mantissa_abs = abs(mantissa)
            exp_str = str(exponent)
            if exp_str.startswith("-"):
                exp_str = exp_str[1:]
            return f"${sign}{mantissa_abs:.{self.precision}f} \\times 10^{{{exp_str}}}$"

        return f"${mantissa:.{self.precision}f} \\times 10^{{{exponent}}}$"


def format_value_sci(value, precision=4):
    """Format a single value in scientific notation for reports."""
    return f"{value:.{precision}e}"
