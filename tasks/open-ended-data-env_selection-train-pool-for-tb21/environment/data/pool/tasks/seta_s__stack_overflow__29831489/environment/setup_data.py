"""Generate sample .npy data files for the pipeline."""

import numpy as np
import os

os.makedirs("data", exist_ok=True)

np.save("data/indices.npy", np.array([1, 0, 3, 2, 3, 0, 1]))
np.save("data/labels.npy", np.array(["dog", "cat", "hamster", "cat", "dog", "hamster"]))
np.save("data/volume.npy", np.random.RandomState(42).randint(0, 4, size=(3, 4, 5)))
np.save("data/word_indices.npy", np.array([2, 0, 3, 1, 2, 0]))

print("Data files created successfully.")
