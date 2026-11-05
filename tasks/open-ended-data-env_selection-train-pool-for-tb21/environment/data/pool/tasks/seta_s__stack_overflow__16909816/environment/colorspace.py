"""Color space conversion utilities for chroma key processing."""

import numpy as np


def rgb_to_ycbcr(r, g, b):
    """Convert normalized RGB values (0.0-1.0 range) to YCbCr color space.

    Uses BT.601 coefficients for conversion.

    Args:
        r, g, b: Red, green, blue values in 0.0-1.0 normalized range

    Returns:
        Tuple of (Y, Cr, Cb) values
    """
    r = np.asarray(r, dtype=np.float64)
    g = np.asarray(g, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)

    Y = 0.2989 * r + 0.5866 * g + 0.1145 * b
    Cr = 0.5647 * (b - Y)
    Cb = 0.7132 * (r - Y)

    return Y, Cr, Cb


def ycbcr_to_rgb(y, cr, cb):
    """Convert YCbCr back to normalized RGB (0.0-1.0 range)."""
    y = np.asarray(y, dtype=np.float64)
    cr = np.asarray(cr, dtype=np.float64)
    cb = np.asarray(cb, dtype=np.float64)

    r = y + 1.4022 * cr
    g = y - 0.3456 * cr - 0.7145 * cb
    b = y + 1.7710 * cb

    r = np.clip(r, 0.0, 1.0)
    g = np.clip(g, 0.0, 1.0)
    b = np.clip(b, 0.0, 1.0)

    return r, g, b
