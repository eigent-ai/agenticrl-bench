"""
KDE-based inverse CDF sampling library.

Fits kernel density estimates to empirical data and generates
new Monte Carlo samples via the inverse CDF method.
"""

import numpy as np
from scipy.stats import gaussian_kde
from scipy.special import ndtr
from scipy.interpolate import interp1d


def fit_kde(data):
    """Fit a Gaussian KDE to 1-D data and return the KDE object."""
    data = np.asarray(data).ravel()
    kde = gaussian_kde(data)
    return kde


def compute_cdf(kde, data, x_grid=None):
    """
    Compute the CDF of the KDE on a grid of x values.

    Uses the closed-form CDF of each Gaussian kernel component
    via the normal CDF (ndtr).

    Parameters
    ----------
    kde : gaussian_kde
        Fitted KDE object.
    data : array-like
        Original data the KDE was fit on.
    x_grid : array-like, optional
        Grid of x values to evaluate the CDF on.

    Returns
    -------
    x_grid : ndarray
    cdf_values : ndarray
    """
    data = np.asarray(data).ravel()
    stdev = kde.covariance[0, 0]

    if x_grid is None:
        x_grid = np.linspace(-5, 5, 1000)

    x_col = x_grid[:, np.newaxis]
    data_row = data[np.newaxis, :]

    cdf_components = ndtr((x_col - data_row) / stdev)
    cdf_values = cdf_components.sum(axis=1)

    return x_grid, cdf_values


def invert_cdf(x_grid, cdf_values):
    """
    Build an interpolating function that maps CDF probabilities
    back to x values (the quantile function).

    Parameters
    ----------
    x_grid : ndarray
        Grid of x values.
    cdf_values : ndarray
        Corresponding CDF values.

    Returns
    -------
    callable
        Interpolating function: probability -> x value.
    """
    inv_func = interp1d(x_grid, cdf_values, kind='linear',
                        bounds_error=False, fill_value='extrapolate')
    return inv_func


def generate_samples(kde, data, n_samples, seed=None):
    """
    Generate Monte Carlo samples using the inverse CDF method.

    Parameters
    ----------
    kde : gaussian_kde
        Fitted KDE object.
    data : array-like
        Original data the KDE was fit on.
    n_samples : int
        Number of samples to generate.
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    ndarray
        Generated samples.
    """
    data = np.asarray(data).ravel()
    x_grid, cdf_values = compute_cdf(kde, data)
    inv_cdf = invert_cdf(x_grid, cdf_values)

    rng = np.random.default_rng(seed)
    u = rng.uniform(0, 1, size=n_samples)
    samples = inv_cdf(u)
    return samples


def fit_lognormal_kde(data):
    """
    Fit a KDE in log-space for log-normal distributed data.

    Parameters
    ----------
    data : array-like
        Positive data assumed to be log-normally distributed.

    Returns
    -------
    kde_log : gaussian_kde
        KDE fitted to log(data).
    log_data : ndarray
        The log-transformed data.
    """
    data = np.asarray(data).ravel()
    log_data = np.log(data)
    kde_log = gaussian_kde(log_data)
    return kde_log, log_data


def generate_samples_lognormal(kde_log, log_data, n_samples, seed=None):
    """
    Generate Monte Carlo samples for log-normal data using the
    inverse CDF method applied in log-space.

    Parameters
    ----------
    kde_log : gaussian_kde
        KDE fitted to log(data).
    log_data : ndarray
        Log-transformed original data.
    n_samples : int
        Number of samples to generate.
    seed : int, optional
        Random seed for reproducibility.

    Returns
    -------
    ndarray
        Generated samples in the original (positive) space.
    """
    samples_log = generate_samples(kde_log, log_data, n_samples, seed=seed)
    return samples_log
