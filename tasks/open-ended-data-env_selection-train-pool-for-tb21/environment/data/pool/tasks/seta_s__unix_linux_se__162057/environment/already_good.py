import math


def calculate_distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.sqrt(dx * dx + dy * dy)


def normalize_vector(x, y):
    length = calculate_distance(0, 0, x, y)
    if length == 0:
        return (0, 0)
    return (x / length, y / length)


def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))


def clamp(value, min_val, max_val):
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value
