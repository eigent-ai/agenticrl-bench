import pandas as pd


def compute_diffs(df):
    """Compute time differences between consecutive entries in a DataFrame.

    Parameters
    ----------
    df : DataFrame with DatetimeIndex

    Returns
    -------
    list : time differences in seconds, with None for the first entry
    """
    diffs = df.index - df.index.shift(1)
    return [None if pd.isna(d) else d.total_seconds() for d in diffs]
