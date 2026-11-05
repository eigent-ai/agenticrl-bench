"""Convert Correlated Color Temperature (CCT) to CIE xy chromaticity coordinates
using the CIE D-series illuminant computation."""

import numpy as np


def CCT_to_xy_CIE_D(T):
    """Compute CIE xy chromaticity from CCT for D-series illuminants.

    Parameters
    ----------
    T : float
        Correlated Color Temperature in Kelvin (4000 <= T <= 25000).

    Returns
    -------
    list of float
        [x, y] chromaticity coordinates.
    """
    if T < 4000 or T > 25000:
        raise ValueError(f"CCT {T} out of range [4000, 25000]")

    # Compute xD
    if T <= 7000:
        xD = (-4.6070e6 / T**3
              + 2.9678e6 / T**2
              + 0.09911e3 / T
              + 0.244063)
    else:
        xD = (-2.0064e9 / T**3
              + 1.9018e6 / T**2
              + 0.24748e3 / T
              + 0.237040)

    # Compute yD
    yD = -3.000 * xD**2 + 2.9700 * xD - 0.27500

    return [xD, yD]
