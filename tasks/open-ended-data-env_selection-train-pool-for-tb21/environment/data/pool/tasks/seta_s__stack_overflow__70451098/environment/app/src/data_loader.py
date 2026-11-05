"""Data loading module for experimental measurements."""

import pandas as pd
import numpy as np


def load_dataset(filepath, column_config):
    """Load a CSV dataset and extract columns based on config mapping.

    Args:
        filepath: Path to CSV file
        column_config: Dict mapping logical names to CSV column names

    Returns:
        Tuple of (data_dict, row_count)
    """
    df = pd.read_csv(filepath)

    result = {}
    for key, col_name in column_config.items():
        try:
            result[key] = df[col_name].values.astype(float)
        except (KeyError, ValueError):
            result[key] = np.full(len(df), np.nan)

    return result, len(df)
