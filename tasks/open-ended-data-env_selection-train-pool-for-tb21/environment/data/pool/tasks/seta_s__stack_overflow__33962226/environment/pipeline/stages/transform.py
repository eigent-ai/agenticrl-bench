import pandas as pd
import numpy as np


def run(data, params):
    """Apply polynomial transformation to numeric columns."""
    method = params.get("method", "polynomial")
    degree = params.get("degree", 2)

    result = data.copy()
    numeric_cols = result.select_dtypes(include="number").columns.tolist()

    if method == "polynomial":
        new_cols = {}
        for col in numeric_cols:
            for d in range(1, degree + 1):
                col_name = f"{col}_d{d}"
                new_cols[col_name] = result[col] ** d
        result = pd.DataFrame(new_cols)

    return result
