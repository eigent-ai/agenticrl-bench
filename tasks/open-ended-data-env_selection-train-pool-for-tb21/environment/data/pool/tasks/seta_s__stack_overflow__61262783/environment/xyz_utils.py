"""CIE XYZ utility functions."""

import numpy as np


def XYZ_to_xy(XYZ):
    """Convert CIE XYZ tristimulus values to xy chromaticity coordinates.

    Parameters
    ----------
    XYZ : array-like
        [X, Y, Z] tristimulus values.

    Returns
    -------
    list of float
        [x, y] chromaticity coordinates.
    """
    X, Y, Z = XYZ[0], XYZ[1], XYZ[2]
    total = X + Y + Z
    x = X / total
    y = Y / total
    return [x, y]
