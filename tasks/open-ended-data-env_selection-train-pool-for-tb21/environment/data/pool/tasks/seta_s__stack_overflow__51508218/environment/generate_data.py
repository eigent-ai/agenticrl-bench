import numpy as np
import os

np.random.seed(42)
x = np.linspace(0, 10, 1000)


def sigmoid(x, scale=1.0):
    return scale / (1 + np.exp(-(x - 5.0)))


os.makedirs('data', exist_ok=True)
scales = [1.0, 2.0, 3.0]
for i, scale in enumerate(scales, 1):
    y = sigmoid(x, scale=scale)
    noise = np.zeros(1000)
    noise[350:650] = np.random.normal(0, 0.25 * scale, 300)
    y += noise
    np.savetxt(
        f'data/curve_0{i}.csv',
        np.column_stack([x, y]),
        delimiter=',',
        header='x,y',
        comments=''
    )

print("Data generation complete.")
