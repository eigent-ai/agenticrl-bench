"""
Scalar field reconstruction from its gradient via numerical path integration.

Given a 2-D scalar field Z sampled on a uniform meshgrid (xl, yl), the module
computes partial derivatives with numpy.gradient, then integrates them back
along a canonical path to recover Z up to a constant, which is fixed by
anchoring to the known corner value Z[0,0].
"""
import numpy as np


def reconstruct_scalar_field(Z, xl, yl):
    """
    Reconstruct scalar field Z from its gradient via cumulative path integration.

    The integration path goes:
      1. Along column 0 (x = xl[0]) from row 0 to row i  — captures y-variation.
      2. Along row i from column 0 to column j            — captures x-variation.

    Parameters
    ----------
    Z   : ndarray, shape (Ny, Nx)  — Z[i, j] = f(yl[i], xl[j])
    xl  : 1-D ndarray, length Nx   — x coordinates, uniform spacing
    yl  : 1-D ndarray, length Ny   — y coordinates, uniform spacing

    Returns
    -------
    Zhat : ndarray, shape (Ny, Nx) — reconstructed scalar field
    """
    stepx = np.diff(xl)[0]
    stepy = np.diff(yl)[0]

    # --- partial derivatives ---
    # np.gradient on a (Ny, Nx) array returns (d/daxis0, d/daxis1) = (dZ/dy, dZ/dx).
    dZdx, dZdy = np.gradient(Z)

    # --- cumulative trapezoidal integration ---
    # SdZx[i, j] approximates integral of dZ/dx from xl[0] to xl[j] along row i.
    # SdZy[i, j] approximates integral of dZ/dy from yl[0] to yl[i] along column j.
    SdZx = np.zeros(Z.shape)
    SdZx[:, 1:] = np.cumsum((dZdx[:, :-1] + dZdx[:, 1:]) / 2.0, axis=1) * stepx

    SdZy = np.zeros(Z.shape)
    SdZy[1:, :] = np.cumsum((dZdy[:-1, :] + dZdy[1:, :]) / 2.0, axis=0) * stepx

    # --- path integration ---
    # Combine: y-path along column 0, then x-path along row i.
    Zhat = SdZy[:, 0:1] + SdZx

    # --- anchor to known corner value ---
    Zhat += Z[0, 0] - Zhat[0, 0]
    return Zhat


def compute_reconstruction_error(Z, Zhat):
    """Return RMSE, max absolute error, and mean absolute error."""
    diff = Z - Zhat
    return {
        "rmse":           float(np.sqrt(np.mean(diff ** 2))),
        "max_abs_error":  float(np.max(np.abs(diff))),
        "mean_abs_error": float(np.mean(np.abs(diff))),
    }
