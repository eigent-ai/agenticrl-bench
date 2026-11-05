import pandas as pd


class NormalizeTransform:
    def __init__(self, columns=None, method="standard", **kwargs):
        self.columns = columns
        self.method = method

    def apply(self, data):
        df = data.copy()
        cols = self.columns or df.select_dtypes(include="number").columns.tolist()
        for col in cols:
            if col in df.columns:
                if self.method == "minmax":
                    min_val = df[col].min()
                    max_val = df[col].max()
                    if max_val != min_val:
                        df[col] = (df[col] - min_val) / (max_val - min_val)
                else:
                    mean_val = df[col].mean()
                    std_val = df[col].std()
                    if std_val != 0:
                        df[col] = (df[col] - mean_val) / std_val
        return df


class EncodeTransform:
    def __init__(self, columns=None, **kwargs):
        self.columns = columns

    def apply(self, data):
        df = data.copy()
        cols = self.columns or df.select_dtypes(include="object").columns.tolist()
        for col in cols:
            if col in df.columns:
                categories = sorted(df[col].unique())
                mapping = {cat: i for i, cat in enumerate(categories)}
                df[col] = df[col].map(mapping)
        return df
