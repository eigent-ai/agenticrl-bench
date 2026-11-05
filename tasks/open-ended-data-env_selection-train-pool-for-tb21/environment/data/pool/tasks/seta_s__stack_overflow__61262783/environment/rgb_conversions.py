"""sRGB color space conversions."""

import numpy as np
from colortemp.srgb_matrix import SRGB_TO_XYZ
from colortemp.xyz_utils import XYZ_to_xy
from colortemp.xy_to_cct import xy_to_CCT_Hernandez1999


def sRGB_to_linear(c):
    """Convert an 8-bit sRGB component (0-255) to linear light.

    Parameters
    ----------
    c : int or float
        sRGB component value in [0, 255].

    Returns
    -------
    float
        Linear-light value in [0, 1].
    """
    return (c / 255.0) ** 2.2


def sRGB_to_XYZ(rgb):
    """Convert an sRGB triplet to CIE XYZ tristimulus values.

    Parameters
    ----------
    rgb : array-like
        [R, G, B] with each component in [0, 255].

    Returns
    -------
    numpy.ndarray
        [X, Y, Z] tristimulus values (Y normalised to ~100 for white).
    """
    linear = np.array([sRGB_to_linear(c) for c in rgb])
    XYZ = SRGB_TO_XYZ @ linear
    return XYZ * 100.0


def sRGB_to_CCT(rgb):
    """Convert an sRGB triplet to Correlated Color Temperature.

    Parameters
    ----------
    rgb : array-like
        [R, G, B] with each component in [0, 255].

    Returns
    -------
    float
        Estimated CCT in Kelvin.
    """
    XYZ = sRGB_to_XYZ(rgb)
    xy = XYZ_to_xy(XYZ)
    return xy_to_CCT_Hernandez1999(xy[0], xy[1])
