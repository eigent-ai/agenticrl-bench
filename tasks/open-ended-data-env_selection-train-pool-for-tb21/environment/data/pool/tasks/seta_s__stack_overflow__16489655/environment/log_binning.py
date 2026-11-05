import numpy as np


def drop_zeros(sequence):
    """Remove zero values from a sequence."""
    return [i for i in sequence if i > 0]


def log_binning(counter_dict, bin_count=35):
    """
    Attempt to log-bin a degree distribution given as a counter dictionary.
    Returns dict with 'x' (bin centers) and 'y' (normalized frequencies).
    """
    keys = drop_zeros(counter_dict.keys())
    values = counter_dict.values()

    max_x = log10(max(keys))
    max_y = log10(max(values))
    max_base = max(max_x, max_y)

    min_x = log10(min(keys))

    bins = np.logspace(min_x, max_base, num=bin_count + 1)

    hist, edges = np.histogram(counter_dict.keys(), bins=bins, density=False)
    bin_means = np.histogram(counter_dict.keys(), bins=bins,
                             weights=counter_dict.values())[0]

    ix = hist > 0
    result_x = ((edges[:-1] + edges[1:]) / 2)[ix]
    result_y = (bin_means[ix] / hist[ix])

    return {
        "x": result_x.tolist(),
        "y": result_y.tolist()
    }
