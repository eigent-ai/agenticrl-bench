"""Statistical aggregation for windowed sensor data."""
import numpy as np


def compute_stat(values, config):
    """Compute the configured statistic over a window of values."""
    statistic = config.get('statistic', 'mean')

    if statistic == 'mean':
        return float(np.nanmean(values))
    elif statistic == 'std':
        return float(np.nanstd(values))
    else:
        raise ValueError(f"Unknown statistic: {statistic}")
