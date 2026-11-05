"""Mandelbrot set computation library.

This package provides tools for computing, analyzing, and visualizing
the Mandelbrot set.
"""

from mandelbrot.core import iterate_point, iterate_vectorized
from mandelbrot.grid import pixel_to_complex, generate_complex_grid
from mandelbrot.render import render_mandelbrot
from mandelbrot.analysis import classify_points, compute_statistics, save_analysis

__all__ = [
    "iterate_point",
    "iterate_vectorized",
    "pixel_to_complex",
    "generate_complex_grid",
    "render_mandelbrot",
    "classify_points",
    "compute_statistics",
    "save_analysis",
]
