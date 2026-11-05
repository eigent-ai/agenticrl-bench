"""Vector norm computation utilities."""

import math


def compute_norm(v):
    """Compute the Euclidean norm of a vector."""
    s = 0.0
    for x in v:
        s += x * x
    return math.sqrt(s)


def compute_norms(vectors):
    """Compute norms for a list of vectors."""
    return [compute_norm(v) for v in vectors]
