import numpy as np
from PIL import Image

arr = np.zeros((40, 80, 4), dtype="uint8")
arr[:, :40, :] = [255, 255, 255, 255]
Image.fromarray(arr, "RGBA").save("watermark.png")

print("Generated watermark")
