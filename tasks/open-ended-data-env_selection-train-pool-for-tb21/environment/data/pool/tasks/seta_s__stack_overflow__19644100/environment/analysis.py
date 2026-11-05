"""Beam analysis functions for structural engineering."""

from engcalc.sections import composite_inertia


def bending_stress(M, y, I):
    """Compute bending stress using the flexure formula.

    sigma = M * y / I

    Args:
        M: bending moment (N*m or lb*in)
        y: distance from neutral axis (m or in)
        I: moment of inertia (m^4 or in^4)

    Returns:
        Bending stress as float
    """
    return float(M * y / I)


def deflection_simply_supported(w, L, E, I):
    """Compute maximum deflection of a simply-supported beam under uniform load.

    delta_max = 5 * w * L^4 / (384 * E * I)

    Args:
        w: distributed load (N/m or lb/in)
        L: span length (m or in)
        E: modulus of elasticity (Pa or psi)
        I: moment of inertia (m^4 or in^4)

    Returns:
        Maximum deflection as float
    """
    return float(5.0 * w * L**4 / (384.0 * E * I))


def moment_of_inertia_composite(shapes):
    """Compute total moment of inertia for a composite section.

    Wrapper around sections.composite_inertia.

    Args:
        shapes: list of section dicts (see composite_inertia)

    Returns:
        Total Ixx as float
    """
    Ixx, Iyy = composite_inertia(shapes)
    return float(Ixx)
