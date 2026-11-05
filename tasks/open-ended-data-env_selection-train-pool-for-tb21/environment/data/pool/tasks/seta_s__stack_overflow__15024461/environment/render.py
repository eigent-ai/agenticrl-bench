"""Rendering functions for Mandelbrot set visualization.

Uses matplotlib with the Agg backend to produce PNG images
of Mandelbrot set iteration data.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def render_mandelbrot(z, iteration_counts, output_path, width, height):
    """Render Mandelbrot set data to a PNG image.

    Parameters
    ----------
    z : np.ndarray
        Final complex z values from the iteration.
    iteration_counts : np.ndarray
        Integer array of iteration counts.
    output_path : str
        Path to save the output PNG image.
    width : int
        Image width for figure sizing.
    height : int
        Image height for figure sizing.
    """
    fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
    ax.imshow(z, cmap='hot', extent=[-2, 1, -1.5, 1.5], aspect='equal')
    ax.set_xlabel('Real')
    ax.set_ylabel('Imaginary')
    ax.set_title('Mandelbrot Set')
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
