import numpy as np
import pandas as pd
import os

os.makedirs('/project/data', exist_ok=True)
np.random.seed(123)
n = 200
feature1 = np.random.uniform(0, 10, n)
feature2 = np.random.uniform(0, 10, n)
noise = np.random.normal(0, 1, n)
target = 2.0 * feature1 + 3.0 * feature2 + noise
pd.DataFrame({'feature1': feature1, 'feature2': feature2, 'target': target}).to_csv('/project/data/regression_data.csv', index=False)
print("Data generated successfully.")
