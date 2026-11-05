import numpy as np
from scipy.linalg import cholesky


def is_diagonally_dominant(A):
    """Check if matrix A is strictly diagonally dominant.

    A matrix is strictly diagonally dominant if for every row,
    the absolute value of the diagonal element is greater than the
    sum of absolute values of the other elements in that row.
    """
    A = np.array(A, dtype=float)
    n = A.shape[0]
    for i in range(n):
        diagonal = abs(A[i, i])
        row_sum = np.sum(np.abs(A[i]))
        if not (diagonal > row_sum):
            return False
    return True


def is_positive_definite(A):
    """Check if matrix A is symmetric positive definite.

    Uses Cholesky decomposition to test positive definiteness.
    First checks symmetry, then attempts decomposition.
    """
    A = np.array(A, dtype=float)
    if A.shape[0] != A.shape[1]:
        return False
    if not (A == A.T).all():
        return False
    try:
        cholesky(A)
        return True
    except Exception:
        return False


def check_convergence_conditions(A):
    """Classify matrix convergence properties.

    Returns a dict indicating whether the matrix is diagonally dominant,
    positive definite, both, or neither.
    """
    A = np.array(A, dtype=float)
    dd = is_diagonally_dominant(A)
    spd = is_positive_definite(A)
    return {
        "diagonally_dominant": dd,
        "positive_definite": spd,
        "both": dd and spd,
        "neither": not dd and not spd
    }
