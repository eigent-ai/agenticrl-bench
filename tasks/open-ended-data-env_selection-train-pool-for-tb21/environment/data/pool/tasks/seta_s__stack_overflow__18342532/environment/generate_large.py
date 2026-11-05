import random
import os

random.seed(42)
os.makedirs("data", exist_ok=True)
with open("data/large_input.txt", "w") as f:
    for _ in range(50000):
        f.write(f"{random.uniform(-200, 200):.6f}\n")
