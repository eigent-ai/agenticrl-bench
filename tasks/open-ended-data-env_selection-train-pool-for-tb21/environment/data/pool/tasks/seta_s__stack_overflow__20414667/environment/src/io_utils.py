"""I/O utilities for loading and saving CSV signal data."""
import numpy as np


def load_csv(path):
    """Load a CSV file into a numpy array.

    Parameters
    ----------
    path : str
        Path to a CSV file with comma-separated numeric values.

    Returns
    -------
    np.ndarray
        2D array of shape (n_samples, n_channels).
    """
    data = np.loadtxt(path, delimiter=",")
    if data.ndim == 1:
        data = data.reshape(-1, 1)
    return data


def save_csv(path, data):
    """Save a numpy array to a CSV file.

    Parameters
    ----------
    path : str
        Output file path.
    data : np.ndarray
        Array to save.
    """
    np.savetxt(path, data, delimiter=",")
