import pandas as pd


def detect_numeric_columns(df):
    """Detect which columns in the DataFrame contain numeric data."""
    numeric_cols = []
    for col in df.columns:
        if any(c.isdigit() for c in str(col)):
            numeric_cols.append(col)
    return numeric_cols
