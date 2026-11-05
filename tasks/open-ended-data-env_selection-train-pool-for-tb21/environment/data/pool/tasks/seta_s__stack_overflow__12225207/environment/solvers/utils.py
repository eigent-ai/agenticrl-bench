import numpy as np


def compute_residual(A, x, b):
    """Compute the residual norm ||Ax - b||."""
    A = np.array(A, dtype=float)
    x = np.array(x, dtype=float)
    b = np.array(b, dtype=float)
    return float(np.linalg.norm(A @ x - b))
