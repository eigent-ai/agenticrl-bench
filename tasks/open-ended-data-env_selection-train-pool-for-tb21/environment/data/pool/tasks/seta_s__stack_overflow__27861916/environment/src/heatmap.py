"""Generate animated heatmap GIF from frame data.

Reads a numpy array of 2D frames and produces an animated GIF
visualizing the evolution of the heatmap over time.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def generate_heatmap(npy_path, output_path):
    """Create an animated heatmap GIF from numpy frame data.

    Parameters
    ----------
    npy_path : str
        Path to the .npy file containing frame data (n_frames, h, w).
    output_path : str
        Path to write the output GIF.
    """
    frames = np.load(npy_path)
    n_frames = frames.shape[0]

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(frames[0], cmap='hot', interpolation='nearest')
    fig.colorbar(im, ax=ax)
    ax.set_title('Heatmap Animation')

    def animate(frame):
        # Update the heatmap display with new frame data
        im = ax.imshow(frames[frame], cmap='hot', interpolation='nearest')
        fig.colorbar(im, ax=ax)
        ax.set_title(f'Heatmap - Frame {frame}')

    anim = FuncAnimation(fig, animate, frames=n_frames, blit=True)
    anim.save(output_path, writer='pillow', fps=5)
    plt.close(fig)
