import os
import numpy as np
from PIL import Image

os.makedirs("test_images", exist_ok=True)

Image.new('L', (64, 64), 128).save("test_images/uniform_gray.jpg", quality=95)

arr = np.tile(np.linspace(0, 255, 64, dtype=np.uint8), (64, 1))
Image.fromarray(arr, mode='L').save("test_images/gradient.jpg", quality=95)

arr = np.zeros((64, 64), dtype=np.uint8)
for r in range(64):
    for c in range(64):
        if ((r // 4) + (c // 4)) % 2 == 0:
            arr[r, c] = 255
Image.fromarray(arr, mode='L').save("test_images/checkerboard.jpg", quality=95)
