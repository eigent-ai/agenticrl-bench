import pandas as pd
import numpy as np


def run(data, params):
    """Normalize specified columns using z-score normalization."""
    columns = params.get("columns", data.columns.tolist())
    epsilon = params.get("epsilon", 0)

    result = data.copy()
    for col in columns:
        if col in result.columns:
            mean = result[col].mean()
            std = result[col].std()
            result[col] = (result[col] - mean) / (std + epsilon)

    return result
