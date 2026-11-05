"""Stripe pattern kernel construction."""

import numpy as np


def build_stripe_kernel(height, width, stripe_width):
    """Build a 2D convolution kernel with alternating +1/-1 horizontal bands.

    Parameters
    ----------
    height : int
        Kernel height in pixels (should match marker height).
    width : int
        Kernel width in pixels (should match marker width).
    stripe_width : int
        Number of rows per stripe band.

    Returns
    -------
    numpy.ndarray
        2D array of shape (height, width) with alternating +1/-1 bands.
    """
    kernel = np.ones((height, width), dtype=np.float64)
    for i in range(2):
        kernel[stripe_width + i :: stripe_width * 2] = -1.0
    return kernel
