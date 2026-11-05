"""Beam analysis functions for structural engineering."""

from engcalc.sections import composite_inertia


def bending_stress(M, y, I):
    return float(M * y / I)


def deflection_simply_supported(w, L, E, I):
    return float(5.0 * w * L**4 / (384.0 * E * I))


def moment_of_inertia_composite(shapes):
    Ixx, Iyy = composite_inertia(shapes)
    return float(Ixx)
