"""Color channel extraction utilities."""

import numpy as np
import cv2


def extract_red_channel(img):
    """Extract redness from an RGB image.

    Computes a per-pixel redness score: R - 0.5*(G+B), clipped to zero.
    """
    bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    r = bgr[:, :, 2].astype(np.float64)
    g = bgr[:, :, 1].astype(np.float64)
    b = bgr[:, :, 0].astype(np.float64)
    red = r - 0.5 * (g + b)
    return np.clip(red, 0, None)


def compute_white_channel(img):
    """Compute brightness/whiteness as the mean of all channels."""
    white = (img[:, :, 0] + img[:, :, 1] + img[:, :, 2]) / 3.0
    return white
