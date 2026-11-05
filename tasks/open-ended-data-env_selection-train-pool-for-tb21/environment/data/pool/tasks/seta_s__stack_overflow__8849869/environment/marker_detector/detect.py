"""Peak detection via 2D convolution."""

import numpy as np
from scipy.signal import convolve2d
from scipy.ndimage import label


def convolve_and_find_peaks(red, white, kernel, threshold):
    """Convolve the color signal with a stripe kernel and extract marker centers.

    Parameters
    ----------
    red : numpy.ndarray
        2D redness map.
    white : numpy.ndarray
        2D whiteness/brightness map.
    kernel : numpy.ndarray
        2D stripe convolution kernel.
    threshold : float
        Detection threshold for the convolution response.

    Returns
    -------
    list[dict]
        List of {"x": int, "y": int} marker center coordinates.
    """
    signal = red - white
    response = convolve2d(signal, kernel, mode="full")

    binary = response > threshold
    labeled, num_features = label(binary)

    results = []
    for i in range(1, num_features + 1):
        component = np.argwhere(labeled == i)
        center = component.mean(axis=0)
        x = int(round(center[0]))
        y = int(round(center[1]))
        results.append({"x": x, "y": y})

    return results
