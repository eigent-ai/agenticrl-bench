"""
Discrete Laplacian utilities providing MATLAB-compatible del2
and a sparse 2D Laplacian matrix builder.
"""
import numpy as np
from scipy import sparse


def matlab_del2(M, *args):
    """
    Compute the discrete Laplacian of M, matching MATLAB's del2().

    For a 2D array with uniform grid spacing h=1, del2(M) equals
    (d²M/dx² + d²M/dy²) / 4.  For non-unit spacing h pass h as an
    extra argument.

    Parameters
    ----------
    M : array_like
        Input array (1-D or 2-D).
    *args : float, optional
        Uniform grid spacing h (default 1.0).  Pass one value for
        isotropic spacing.

    Returns
    -------
    numpy.ndarray
        Discrete Laplacian divided by (2 * ndim * h²).
    """
    M = np.asarray(M, dtype=float)
    num_dims = M.ndim

    if len(args) == 0:
        h = [1.0] * num_dims
    elif len(args) == 1:
        h = [float(args[0])] * num_dims
    else:
        h = [float(a) for a in args[:num_dims]]

    result = np.zeros_like(M, dtype=float)

    for dim in range(num_dims):
        ax = np.moveaxis(M, dim, 0)
        rx = np.moveaxis(result, dim, 0)
        n = ax.shape[0]
        hd = h[dim]

        # Interior: standard central-difference second derivative
        if n >= 3:
            rx[1:-1] += (ax[:-2] - 2.0 * ax[1:-1] + ax[2:]) / hd ** 2

        # Boundary: one-sided finite difference
        if n >= 3:
            rx[0]  += (ax[0] - 2.0 * ax[1] + ax[2])       / hd ** 2
            rx[-1] += (ax[-3] - 2.0 * ax[-2] + ax[-1])    / hd ** 2

    # Divide by number of dimensions to get MATLAB-normalised result
    return result / num_dims


def build_laplacian_matrix(nx, ny):
    """
    Build the sparse 2D Laplacian matrix for an nx × ny grid.

    Uses the standard 5-point stencil.  Nodes are numbered row-major:
    node (i, j) has index i*nx + j.  No periodic boundary conditions.

    Parameters
    ----------
    nx : int
        Number of grid points in x (columns).
    ny : int
        Number of grid points in y (rows).

    Returns
    -------
    scipy.sparse.csr_matrix
        Sparse Laplacian of shape (nx*ny, nx*ny).
    """
    N = nx * ny
    main_diag    = np.ones(N) * -4.0
    side_diag    = np.ones(N - 1)
    side_diag[np.arange(1, N) % (nx + 1) == 0] = 0   # zero cross-boundary links
    up_down_diag = np.ones(N - nx)

    diagonals = [main_diag, side_diag, side_diag, up_down_diag, up_down_diag]
    laplacian = sparse.diags(diagonals, [0, -1, 1, nx, -nx], format="csr")
    return laplacian
