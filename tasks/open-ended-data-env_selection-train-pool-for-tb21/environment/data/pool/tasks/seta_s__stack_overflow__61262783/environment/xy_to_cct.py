"""Estimate CCT from CIE xy chromaticity using McCamy's approximation."""

import numpy as np


def xy_to_CCT_Hernandez1999(x, y):
    """Estimate Correlated Color Temperature from xy chromaticity.

    Uses McCamy's cubic polynomial approximation.

    Parameters
    ----------
    x : float
        CIE x chromaticity coordinate.
    y : float
        CIE y chromaticity coordinate.

    Returns
    -------
    float
        Estimated CCT in Kelvin.
    """
    xe = 0.3366
    ye = 0.1735
    n = (x - xe) / (y - ye)

    CCT = (-449.0 * n**3 + 3525.0 * n**2 - 6823.3 * n + 5520.33)
    return CCT
