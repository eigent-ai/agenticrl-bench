"""sRGB to CIE XYZ conversion matrix (IEC 61966-2-1)."""

import numpy as np

# sRGB linear to CIE XYZ (D65 reference white)
SRGB_TO_XYZ = np.array([
    [0.4124564, 0.3575761, 0.1804375],
    [0.2126729, 0.7151522, 0.0721750],
    [0.0193339, 0.1191920, 0.9503041],
])
