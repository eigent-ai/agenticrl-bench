"""Matrix construction utilities for the FE solver pipeline.

Handles loading sparse matrices from triplet files and constructing
scipy sparse matrix objects.
"""
import numpy as np
import scipy.sparse as sp


def load_triplets(path):
    """Load sparse matrix data from a triplet file.

    File format:
        Line 1: integer N (matrix dimension)
        Lines 2+: row col value  (indices are 1-based, Matlab convention)

    Returns:
        I, J, V (arrays of row indices, column indices, values)
        n (matrix dimension)
    """
    with open(path, "r") as f:
        n = int(f.readline().strip())
        data = np.loadtxt(f)

    I = data[:, 0].astype(int)
    J = data[:, 1].astype(int)
    V = data[:, 2]

    return I, J, V, n


def build_sparse_matrix(I, J, V, n):
    """Construct a sparse matrix from triplet (COO) data.

    Parameters:
        I: row indices
        J: column indices
        V: values
        n: matrix dimension (n x n)

    Returns:
        Sparse matrix
    """
    mat = sp.coo_matrix((V, (I, J)))
    return mat
