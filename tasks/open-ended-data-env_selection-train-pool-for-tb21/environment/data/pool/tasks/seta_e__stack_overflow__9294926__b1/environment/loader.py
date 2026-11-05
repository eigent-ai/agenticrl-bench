import pandas as pd


def load_csv(filepath):
    """Load a single CSV sales file and return a DataFrame."""
    df = pd.read_csv(filepath, engine='pyarrow')
    return df
