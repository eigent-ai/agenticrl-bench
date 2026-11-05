"""
ORCA-3D: Optimal Reciprocal Collision Avoidance geometry helpers (3D).

Implements the minimum-change velocity vector for truncated-cone velocity
obstacles, following:
  van den Berg et al., "Reciprocal n-Body Collision Avoidance" (2011)
  RVO2-3D reference implementation by Jur van den Berg and Stephen J. Guy
"""

import numpy as np
from numpy.typing import NDArray


def _abs_sq(v: NDArray) -> float:
    """Squared Euclidean length of vector v."""
    return float(np.dot(v, v))


def compute_velocity_obstacle(
    rel_pos: NDArray,
    rel_vel: NDArray,
    combined_radius: float,
    time_horizon: float,
) -> dict:
    """
    Compute the minimum-change velocity vector **u** such that
    ``rel_vel + u`` lies on the boundary of the truncated-cone velocity
    obstacle defined by two spherical agents.

    Parameters
    ----------
    rel_pos : ndarray, shape (3,)
        Relative position: other.position - self.position.
    rel_vel : ndarray, shape (3,)
        Relative velocity: self.velocity - other.velocity.
    combined_radius : float
        Sum of agent radii (r_A + r_B).  Must be positive.
    time_horizon : float
        Collision lookahead time (seconds).  The cutoff sphere centre is
        at ``rel_pos / time_horizon`` with radius
        ``combined_radius / time_horizon``.  Must be positive.

    Returns
    -------
    dict with keys
        'u'      : ndarray (3,) — minimum-change velocity vector
        'normal' : ndarray (3,) — unit outward normal of VO boundary at contact
        'region' : 'cutoff' | 'cone'
    """
    dist_sq = _abs_sq(rel_pos)
    cr_sq = combined_radius ** 2

    # Scale factor: cutoff sphere centre is at tau * rel_pos
    tau = time_horizon

    # w = vector from cutoff centre to relative velocity
    w = rel_vel - tau * rel_pos
    w_len_sq = _abs_sq(w)
    dot_wp = float(np.dot(w, rel_pos))

    # Classify: cutoff-circle region vs cone-surface region.
    # Cutoff condition: w points "backward" past the cutoff sphere.
    if dot_wp > 0.0 and dot_wp ** 2 > cr_sq * w_len_sq:
        # ── Project onto cut-off circle ──────────────────────────────────
        w_len = float(np.sqrt(w_len_sq))
        unit_w = w / w_len
        u = (combined_radius * tau - w_len) * unit_w
        normal = unit_w
        region = 'cutoff'
    else:
        # ── Project onto cone surface ─────────────────────────────────────
        # Solve the quadratic  a*t^2 - 2b*t + c_coeff = 0  for t, where t
        # is the scale factor such that t*rel_pos is the tangency point on
        # the big sphere, then recover the tangent velocity direction.
        a = dist_sq
        b = float(np.dot(rel_pos, rel_vel))
        cross_pv = np.cross(rel_pos, rel_vel)
        c = _abs_sq(rel_vel) - _abs_sq(cross_pv) / (dist_sq + cr_sq)

        discriminant = b ** 2 - a * c
        if discriminant < 0.0:
            discriminant = 0.0
        t = (b + float(np.sqrt(discriminant))) / a

        ww = rel_vel - t * rel_pos
        ww_len = float(np.linalg.norm(ww))
        if ww_len < 1e-10:
            ww_len = 1e-10          # guard against zero-length ww
        unit_ww = ww / ww_len
        u = (combined_radius * t - ww_len) * unit_ww
        normal = unit_ww
        region = 'cone'

    return {'u': u, 'normal': normal, 'region': region}
