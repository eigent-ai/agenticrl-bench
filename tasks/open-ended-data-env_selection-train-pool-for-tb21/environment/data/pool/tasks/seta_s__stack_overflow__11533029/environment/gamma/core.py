import numpy as np


def gamma2d(reference, evaluation, dta=3, dose_thresh=0.03):
    """Compute 2D gamma index array.

    Parameters
    ----------
    reference : ndarray
        Reference dose map.
    evaluation : ndarray
        Evaluation dose map (same shape as reference).
    dta : int
        Distance-to-agreement in pixel units.
    dose_thresh : float
        Dose difference threshold as a fraction (e.g. 0.03 for 3%).

    Returns
    -------
    ndarray
        Gamma index map with the same shape as the input arrays.
    """
    size = reference.shape
    gamma_map = np.full(size, np.inf)
    dosed = dose_thresh

    for i in range(size[0]):
        for j in range(size[1]):
            i_min, i_max = max(0, i - dta), i + dta
            j_min, j_max = max(0, j - dta), j + dta

            min_gamma = np.inf
            for k in range(i_min, i_max):
                for l in range(j_min, j_max):
                    r2 = (i - k) ** 2 + (j - l) ** 2
                    d2 = (reference[i, j] - evaluation[k, l]) ** 2
                    g = np.sqrt(r2 / dta + d2 / dosed)
                    if g < min_gamma:
                        min_gamma = g
            gamma_map[i, j] = min_gamma
    return gamma_map
