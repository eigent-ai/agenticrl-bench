from sklearn.datasets import make_classification
import pandas as pd
import numpy as np

np.random.seed(42)
X, y = make_classification(n_samples=300, n_features=6, n_informative=3,
                           n_redundant=1, n_clusters_per_class=1,
                           n_classes=3, random_state=42)
df = pd.DataFrame(X, columns=[f'f{i+1}' for i in range(6)])
df['label'] = y
df.to_csv('dataset.csv', index=False)
