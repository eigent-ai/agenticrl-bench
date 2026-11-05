"""Frequency-domain transforms for 8x8 block processing."""
import numpy as np
from scipy.fft import dstn, idstn

def forward_transform(block):
    """Apply forward frequency transform to an 8x8 block."""
    return dstn(block, type=2, norm='ortho')

def inverse_transform(block):
    """Apply inverse frequency transform to an 8x8 block."""
    return idstn(block, type=2, norm='ortho')
