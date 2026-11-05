"""Module D — Numeric validation routines."""


def is_positive(value):
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def clamp(value, lo, hi):
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value
