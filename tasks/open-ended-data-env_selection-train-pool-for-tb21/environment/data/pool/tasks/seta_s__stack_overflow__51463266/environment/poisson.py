"""Poisson disk sampling for starfield generation.

Generates points with a guaranteed minimum distance between any two points.
Uses Bridson's algorithm with active-list rejection sampling to efficiently
place points while maintaining the minimum distance constraint.
"""

import math
import random


def _distance(p1, p2):
    """Compute Euclidean distance between two points."""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return math.sqrt(dx * dx + dy * dy)


def generate(width, height, num_points, min_distance=30, **kwargs):
    """Generate points using Poisson disk sampling.

    Args:
        width: Rectangle width.
        height: Rectangle height.
        num_points: Number of points to generate.
        min_distance: Minimum allowed distance between any two points.

    Returns:
        List of (x, y) tuples.
    """
    max_attempts = 5
    cell_size = min_distance / math.sqrt(2)
    grid_w = int(math.ceil(width / cell_size))
    grid_h = int(math.ceil(height / cell_size))

    grid = {}

    def _grid_key(p):
        return (int(p[0] / cell_size), int(p[1] / cell_size))

    def _is_valid(candidate):
        gx, gy = _grid_key(candidate)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                key = (gx + dx, gy + dy)
                if key in grid:
                    dist = _distance(candidate, grid[key])
                    if dist < min_distance ** 2:
                        return False
        return True

    first = (random.uniform(0, width), random.uniform(0, height))
    points = [first]
    grid[_grid_key(first)] = first
    active = [first]

    while active and len(points) < num_points:
        idx = random.randint(0, len(active) - 1)
        source = active[idx]
        found = False

        for _ in range(max_attempts):
            angle = random.uniform(0, 2 * math.pi)
            r = random.uniform(min_distance, 2 * min_distance)
            cx = source[0] + r * math.cos(angle)
            cy = source[1] + r * math.sin(angle)
            candidate = (cx, cy)

            if 0 <= cx <= width and 0 <= cy <= height and _is_valid(candidate):
                points.append(candidate)
                grid[_grid_key(candidate)] = candidate
                active.append(candidate)
                found = True
                break

        if not found:
            active.pop(idx)

    return points[:num_points]
