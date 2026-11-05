import numpy as np


def analyze_convergence(residuals_history):
    """Analyze convergence behavior from residual history.

    Computes convergence rate and detects stalling based on
    recent residual changes relative to the overall trend.

    Parameters
    ----------
    residuals_history : list of float
        Residual norms from each iteration.

    Returns
    -------
    dict
        Analysis results with status, stalled flag, and convergence rate.
    """
    if not residuals_history or len(residuals_history) < 2:
        return {"status": "insufficient_data", "stalled": False, "rate": None}

    residuals = np.array(residuals_history, dtype=float)

    ratios = residuals[1:] / residuals[:-1]
    log_ratios = np.log(ratios)
    avg_log_rate = np.mean(log_ratios)
    rate = float(np.exp(avg_log_rate))

    window = min(10, len(residuals) // 2)
    if window < 2:
        return {"status": "converging", "stalled": False, "rate": rate}

    recent = residuals[-window:]
    threshold = np.mean(residuals) * 0.01
    changes = np.abs(np.diff(recent))
    stalled = bool(np.all(changes < threshold))

    if residuals[-1] < 1e-10:
        status = "converged"
    elif stalled:
        status = "stalled"
    elif rate > 1.0:
        status = "diverging"
    else:
        status = "converging"

    return {"status": status, "stalled": stalled, "rate": rate}
