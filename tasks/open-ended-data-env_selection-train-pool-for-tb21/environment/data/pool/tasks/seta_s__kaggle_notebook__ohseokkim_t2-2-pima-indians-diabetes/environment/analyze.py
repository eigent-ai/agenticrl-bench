import pandas as pd

df = pd.read_csv('/data/diabetes.csv')
print(f'Shape: {df.shape}')
print(df.dtypes)
print(df.describe())
