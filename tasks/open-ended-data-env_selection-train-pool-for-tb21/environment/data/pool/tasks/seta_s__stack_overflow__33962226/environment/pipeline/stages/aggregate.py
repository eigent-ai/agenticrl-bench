import pandas as pd
import numpy as np


def run(data, params):
    """Aggregate data into a single summary column."""
    method = params.get("method", "mean")

    values = data.values.squeeze()
    series = pd.Series(values)

    if method == "mean":
        result_val = series.rolling(window=min(5, len(series))).mean()
    elif method == "sum":
        result_val = series.rolling(window=min(5, len(series))).sum()
    else:
        result_val = series

    result = pd.DataFrame({"aggregated": result_val})
    return result
