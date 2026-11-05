import os
import pandas as pd
from sklearn.datasets import make_classification

X, y = make_classification(
    n_samples=500, n_features=10, n_informative=6, n_redundant=2, random_state=42
)
df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(10)])
df["target"] = y
os.makedirs("data", exist_ok=True)
df.to_csv("data/dataset.csv", index=False)
print("Dataset generated: data/dataset.csv")
