import numpy as np


def compute_pass_rate(gamma_map, threshold=1.0):
    """Compute the percentage of points passing the gamma criterion.

    Parameters
    ----------
    gamma_map : ndarray
        Gamma index values.
    threshold : float
        Acceptance threshold (default 1.0).

    Returns
    -------
    float
        Pass rate as a percentage (0-100).
    """
    valid = gamma_map[~np.isinf(gamma_map)]
    if len(valid) == 0:
        return 0.0
    passing = np.sum(valid < threshold)
    return float(passing / len(valid) * 100)


def build_entry(pair_name, gamma_map, pass_rate):
    """Build a report entry dict for a single dose map pair."""
    valid = gamma_map[~np.isinf(gamma_map)]
    return {
        "pair_name": pair_name,
        "pass_rate": pass_rate,
        "mean_gamma": float(np.mean(valid)) if len(valid) > 0 else None,
        "max_gamma": float(np.max(valid)) if len(valid) > 0 else None,
        "gamma_map_shape": list(gamma_map.shape),
    }
