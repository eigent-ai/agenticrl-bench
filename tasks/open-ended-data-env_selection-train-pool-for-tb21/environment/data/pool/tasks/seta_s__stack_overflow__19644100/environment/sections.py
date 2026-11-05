"""Cross-section property calculations for structural engineering."""

import math


def rectangle_inertia(b, h):
    """Compute moments of inertia for a rectangle.

    Args:
        b: width
        h: height

    Returns:
        (Ixx, Iyy) tuple of moments of inertia about centroidal axes
    """
    Ixx = (b * h**3) / 12.0
    Iyy = (h * b**3) / 12.0
    return (Ixx, Iyy)


def circle_inertia(r):
    """Compute moments of inertia for a circle.

    Args:
        r: radius

    Returns:
        (Ixx, Iyy) tuple - both equal for a circle
    """
    I = (math.pi * r**4) / 4.0
    return (I, I)


def composite_inertia(sections):
    """Compute composite moment of inertia using the parallel axis theorem.

    Args:
        sections: list of dicts with keys:
            'Ixx': local moment of inertia about own centroid (x-axis)
            'Iyy': local moment of inertia about own centroid (y-axis)
            'area': cross-sectional area
            'cx': centroid x-coordinate
            'cy': centroid y-coordinate

    Returns:
        (Ixx_total, Iyy_total) about the composite centroid
    """
    total_area = sum(s['area'] for s in sections)
    cx_bar = sum(s['area'] * s['cx'] for s in sections) / total_area
    cy_bar = sum(s['area'] * s['cy'] for s in sections) / total_area

    Ixx_total = 0.0
    Iyy_total = 0.0
    for s in sections:
        dy = s['cy'] - cy_bar
        dx = s['cx'] - cx_bar
        Ixx_total += s['Ixx'] + s['area'] * dy**2
        Iyy_total += s['Iyy'] + s['area'] * dx**2

    return (Ixx_total, Iyy_total)


def thin_wall_tube(r, t):
    """Approximate moment of inertia and area for a thin-walled circular tube.

    Uses thin-wall approximation (valid when t << r):
        Ixx ~ pi * r^3 * t
        area ~ 2 * pi * r * t

    Args:
        r: mean radius
        t: wall thickness

    Returns:
        (Ixx, area) tuple
    """
    Ixx = math.pi * r**3 * t
    area = 2.0 * math.pi * r * t
    return (Ixx, area)
