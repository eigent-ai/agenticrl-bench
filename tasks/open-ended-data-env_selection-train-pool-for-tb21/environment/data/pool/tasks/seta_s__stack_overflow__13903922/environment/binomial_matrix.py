"""Binomial probability matrix generator."""

import numpy as np
from scipy.stats import binom


def build_binomial_matrix(N, p):
    """Build a matrix M where M[k, n] = P(X=k | n, p) for k=0..N, n=0..N.

    Args:
        N: maximum number of trials
        p: success probability

    Returns:
        numpy.ndarray: (N+1) x (N+1) matrix of binomial probabilities
    """
    k = np.arange(N + 1)[:, None]
    n = np.arange(N + 1)[None, :]
    M = binom.pmf(n, k, p)
    return M
