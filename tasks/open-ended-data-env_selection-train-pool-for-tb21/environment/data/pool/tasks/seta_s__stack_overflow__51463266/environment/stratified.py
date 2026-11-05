"""Stratified (grid-based) random sampling for starfield generation.

Divides the rectangle into a grid of cells and places one or more random
points within each cell. This ensures spatial coverage across the entire
area while maintaining a natural random appearance.
"""

import math
import random


def generate(width, height, num_points, **kwargs):
    """Generate points using stratified sampling.

    Args:
        width: Rectangle width.
        height: Rectangle height.
        num_points: Number of points to generate.

    Returns:
        List of (x, y) tuples.
    """
    cols = max(1, int(math.ceil(math.sqrt(num_points * width / height))))
    rows = max(1, int(math.ceil(num_points / cols)))

    cell_w = width / cols
    cell_h = height / rows

    points = []
    for i in range(num_points):
        col = i % cols
        row = i // cols

        x = random.uniform(col * cell_w, col * cell_w + width)
        y = random.uniform(row * cell_h, row * cell_h + height)

        points.append((x, y))

    return points
