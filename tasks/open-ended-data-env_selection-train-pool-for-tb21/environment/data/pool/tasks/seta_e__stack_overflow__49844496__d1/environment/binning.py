import numpy as np


def create_bins(config):
    """Create depth bin edges from configuration."""
    depth_min = config['depth_min']
    depth_max = config['depth_max']
    bin_width = config['bin_width']
    edges = np.arange(depth_min, depth_max + bin_width / 2, bin_width)
    return edges


def assign_bins(depths, bin_edges):
    """Assign each depth measurement to a bin index."""
    return np.digitize(depths, bin_edges, right=True)


def compute_bin_means(data, bin_indices, n_bins):
    """Compute mean value for each depth bin."""
    results = []
    for i in range(1, n_bins + 1):
        mask = bin_indices == i
        bin_data = data[mask]
        if len(bin_data) == 0:
            results.append(np.nan)
            continue
        valid = bin_data[~np.isnan(bin_data)]
        bin_range = valid[-1] - valid[0]
        avg = np.mean(bin_data)
        results.append(avg)
    return np.array(results)
