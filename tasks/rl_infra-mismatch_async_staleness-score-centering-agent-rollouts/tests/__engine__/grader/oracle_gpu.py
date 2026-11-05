import math
import numpy as np
from oracle import EPS, _alpha, _f, _head_mass
def logsumexp(values):
    m = max(values)
    return m + math.log(sum(math.exp(v - m) for v in values))
def token_gradient_dense(ro, r, kz, lse, *, A, mode, is_mode, cp_scale):
    T = ro.temperature
    ids, _, _ = ro.kept(r)
    p = np.exp(np.asarray(kz, dtype=np.float64) / T - lse)
    pos = {int(t): i for i, t in enumerate(ids)}
    y = int(ro.a["out_ids"][r])
    iy = pos[y]
    vec = np.zeros(len(ids))
    if mode == "support":
        o = ro.a["sup_off"]
        S = ro.a["sup_ids"][o[r]:o[r + 1]]
        qS = np.exp(ro.a["sup_logp"][o[r]:o[r + 1]].astype(np.float64))
        iS = np.array([pos[int(t)] for t in S])
        pS = p[iS] / p[iS].sum()
        jy = int(np.where(S == y)[0][0])
        w = _f(is_mode, pS[jy] / qS[jy])
        rho = max(1 - qS.sum(), EPS) / max(1 - pS.sum(), EPS)
        c = _head_mass(is_mode, pS, qS) - _alpha(is_mode, rho) * pS
        pi = np.zeros(len(ids))
        pi[iS] = pS
        vec[iy] += w
        np.subtract.at(vec, iS, c)
        vec -= (w - c.sum()) * pi
        tail_mult = 0.0
    else:
        valid = ro.a["top_ids"][r] >= 0
        H = ro.a["top_ids"][r][valid]
        qH = np.exp(ro.a["top_logp"][r][valid].astype(np.float64))
        iH = np.array([pos[int(t)] for t in H])
        pH = p[iH]
        q_y = math.exp(float(ro.a["out_logp"][r]))
        w = _f(is_mode, p[iy] / q_y)
        rho = max(1 - qH.sum(), EPS) / max(1 - pH.sum(), EPS)
        c = _head_mass(is_mode, pH, qH) - _alpha(is_mode, rho) * pH
        vec[iy] += w
        np.subtract.at(vec, iH, c)
        vec -= (w - c.sum()) * p
        tail_mult = -(w - c.sum())
    scale = -A * cp_scale / T
    return ids, vec * scale, tail_mult * scale
