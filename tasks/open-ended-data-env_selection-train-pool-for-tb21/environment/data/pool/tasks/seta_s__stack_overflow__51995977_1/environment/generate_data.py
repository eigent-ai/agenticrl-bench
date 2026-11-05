import os
import numpy as np

def main():
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    rng = np.random.RandomState(42)

    batch_001 = rng.randint(0, 256, size=(16, 224, 224), dtype=np.uint8)
    np.save("data/raw/batch_001.npy", batch_001)

    batch_002 = rng.randint(0, 256, size=(16, 224, 224), dtype=np.uint8)
    np.save("data/raw/batch_002.npy", batch_002)

    batch_003 = rng.randint(0, 256, size=(8, 228, 228), dtype=np.uint8)
    np.save("data/raw/batch_003.npy", batch_003)

    print("Generated raw data batches.")

if __name__ == "__main__":
    main()
