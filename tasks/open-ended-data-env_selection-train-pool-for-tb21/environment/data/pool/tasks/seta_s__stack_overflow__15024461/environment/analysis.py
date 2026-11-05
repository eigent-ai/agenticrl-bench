"""Analysis functions for Mandelbrot set computation results.

Provides point classification and statistical analysis of
iteration count data.
"""

import json
import numpy as np
from mandelbrot.core import iterate_point


def classify_points(points, max_iter=100):
    """Classify a list of complex numbers as in or out of the Mandelbrot set.

    A point is considered in the set if its iteration count equals max_iter
    (i.e., it did not escape within the allowed iterations).

    Parameters
    ----------
    points : list of complex
        Complex numbers to classify.
    max_iter : int
        Maximum iteration count.

    Returns
    -------
    dict
        Mapping from string representation of each point to bool
        (True if in the Mandelbrot set).
    """
    results = {}
    for c in points:
        count = iterate_point(c.real, c.imag, max_iter)
        results[str(c)] = (count == max_iter)
    return results


def compute_statistics(iteration_counts, max_iter=100):
    """Compute summary statistics from iteration count data.

    Parameters
    ----------
    iteration_counts : np.ndarray
        2D integer array of iteration counts.
    max_iter : int
        The maximum iteration count used during computation.

    Returns
    -------
    dict
        Dictionary with keys: in_set_count, total_points,
        in_set_fraction, boundary_count.
    """
    total = iteration_counts.size
    in_set = int(np.sum(iteration_counts == max_iter))
    boundary = int(np.sum((iteration_counts >= 10) & (iteration_counts < max_iter)))
    return {
        "in_set_count": in_set,
        "total_points": total,
        "in_set_fraction": round(in_set / total, 6),
        "boundary_count": boundary,
    }


def save_analysis(output_path, statistics, classifications):
    """Save analysis results to a JSON file.

    Parameters
    ----------
    output_path : str
        Path to write the JSON file.
    statistics : dict
        Statistics from compute_statistics().
    classifications : dict
        Point classifications from classify_points().
    """
    data = {**statistics, "point_classifications": classifications}
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
