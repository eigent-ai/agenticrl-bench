import numpy as np


def gauss_seidel(A, b, x0=None, max_iter=1000, tol=1e-10):
    """Gauss-Seidel iterative solver for Ax = b.

    Parameters
    ----------
    A : array_like
        Coefficient matrix.
    b : array_like
        Right-hand side vector.
    x0 : array_like, optional
        Initial guess. Defaults to zeros.
    max_iter : int
        Maximum number of iterations.
    tol : float
        Convergence tolerance on residual norm.

    Returns
    -------
    x : ndarray
        Solution vector.
    iterations : int
        Number of iterations performed.
    converged : bool
        Whether the solver converged within tolerance.
    residuals : list of float
        Residual norm history.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    x = x0.copy() if x0 is not None else np.zeros(n)
    residuals = []

    for k in range(max_iter):
        x_old = x.copy()
        x_new = x.copy()
        for i in range(n):
            sigma = 0.0
            for j in range(n):
                if j != i:
                    sigma += A[i, j] * x_old[j]
            x_new[i] = (b[i] - sigma) / A[i, i]
        x = x_new.copy()

        residual = float(np.linalg.norm(A @ x - b))
        residuals.append(residual)

        if residual < tol:
            return x, k + 1, True, residuals

    return x, max_iter, False, residuals
