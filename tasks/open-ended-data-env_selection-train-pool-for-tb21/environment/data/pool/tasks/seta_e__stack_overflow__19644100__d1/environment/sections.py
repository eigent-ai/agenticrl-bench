"""Cross-section property calculations for structural engineering."""

import math


def rectangle_inertia(b, h):
    Ixx = (b * h**3) / 12.0
    Iyy = (h * b**3) / 12.0
    return (Ixx, Iyy)


def circle_inertia(r):
    I = (math.pi * r**4) / 4.0
    return (I, I)


def composite_inertia(sections):
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
    Ixx = math.pi * r**3 * t
    area = 2.0 * math.pi * r * t
    return (Ixx, area)
