"""Generate deterministic test images."""
import numpy as np

def write_pgm(path, image):
    h, w = image.shape
    with open(path, 'wb') as f:
        f.write(f'P5\n{w} {h}\n255\n'.encode())
        f.write(image.astype(np.uint8).tobytes())

rng = np.random.RandomState(42)

# 256x256 image with gradients, edges, and texture
img1 = np.zeros((256, 256), dtype=np.float64)
for i in range(256):
    img1[:, i] += i
for i in range(0, 256, 32):
    for j in range(0, 256, 32):
        img1[i:i+16, j:j+16] += 60
img1 += rng.normal(0, 10, (256, 256))
img1 = np.clip(img1, 0, 255)
write_pgm('samples/test_photo.pgm', img1)

# 200x150 image (not multiple of 8)
img2 = np.zeros((150, 200), dtype=np.float64)
for i in range(150):
    img2[i, :] += i * 255.0 / 150
cy, cx = 75, 100
Y, X = np.mgrid[:150, :200]
dist = np.sqrt((X - cx)**2 + (Y - cy)**2)
img2 += 80 * np.sin(dist / 10)
img2 += rng.normal(0, 8, (150, 200))
img2 = np.clip(img2, 0, 255)
write_pgm('samples/test_small.pgm', img2)

print("Sample images generated.")
