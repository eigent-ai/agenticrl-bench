import pandas as pd


def load_csv(filepath):
    """Load a CSV file into a DataFrame."""
    return pd.read_csv(filepath)
