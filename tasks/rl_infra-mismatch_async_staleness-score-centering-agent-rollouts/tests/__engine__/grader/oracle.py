import math
import numpy as np
EPS = 1e-6
def _f(mode, r, clip=2.0, low=0.5, high=5.0):
    if mode == "none":
        return 1.0
    if mode == "tis":
        return min(r, clip)
    lr = math.log(r) if r > 0 else -math.inf
    return r if (math.log(low) <= lr <= math.log(high)) else 0.0
def _head_mass(mode, p, q, clip=2.0, low=0.5, high=5.0):
    if mode == "none":
        return q.copy()
    if mode == "tis":
        return np.minimum(p, clip * q)
    with np.errstate(divide="ignore"):
        lr = np.log(p) - np.log(q)
    inside = (lr >= math.log(low)) & (lr <= math.log(high))
    return np.where(inside, p, 0.0)
def _alpha(mode, rho, clip=2.0, low=0.5, high=5.0):
    if mode == "none":
        return rho
    if mode == "tis":
        return min(clip * rho, 1.0)
    return float((rho >= 1.0 / high) and (rho <= 1.0 / low))
def token_gradient(ro, r, *, A, mode, is_mode, cp_scale, vocab):
    T = ro.temperature
    ids, z, fill = ro.kept(r)
    u = z.astype(np.float64) / T
    uf = float(fill) / T
    n_tail = vocab - len(ids)
    m = max(u.max(), uf)
    lse = m + math.log(np.exp(u - m).sum() + n_tail * math.exp(uf - m))
    p = np.exp(u - lse)
    p_fill = math.exp(uf - lse)
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
        q_y = qS[jy]
        pi_y = pS[jy]
        w = _f(is_mode, pi_y / q_y)
        rho = max(1 - qS.sum(), EPS) / max(1 - pS.sum(), EPS)
        c = _head_mass(is_mode, pS, qS) - _alpha(is_mode, rho) * pS
        pi = np.zeros(len(ids))
        pi[iS] = pS
        vec[iy] += w
        np.subtract.at(vec, iS, c)
        vec -= (w - c.sum()) * pi
        tail = 0.0
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
        tail = -(w - c.sum()) * p_fill
    scale = -A * cp_scale / T
    return ids, vec * scale, tail * scale
