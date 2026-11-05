"""Michaelis-Menten substrate depletion: dS/dt = -vmax*S/(Ks+S)"""

import numpy as np
from scipy.integrate import solve_ivp


def solve_michaelis_menten(config):
    vmax = config['vmax']
    Ks = config['Ks']
    S0 = config['S0']
    t_start = config['t_start']
    t_end = config['t_end']
    n_points = config['n_points']

    t_eval = np.linspace(t_start, t_end, n_points)

    def ode_func(t, S):
        return [-vmax * S[0] / (Ks + S[0])]

    sol = solve_ivp(ode_func, [t_start, t_end], [S0], t_eval=t_eval, method='RK45')

    if not sol.success:
        raise RuntimeError(f"Michaelis-Menten solver failed: {sol.message}")

    return {
        't': sol.t.tolist(),
        'S': sol.y[0].tolist()
    }
