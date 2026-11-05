"""Utility functions for the activity pipeline."""

import pandas as pd


def filter_short_sessions(df, max_duration=3600.0):
    """Return sessions with duration under max_duration seconds.

    Parameters
    ----------
    df : DataFrame with a 'session_duration' timedelta column
    max_duration : maximum duration in seconds (float)
    """
    mask = df["session_duration"] < max_duration
    return df[mask].copy()


def find_nearest_session(df, target_seconds=600.0):
    """Find the session whose duration is closest to target_seconds.

    Computes absolute difference between each session duration and the target.
    """
    durations = df["session_duration"]
    diffs = (durations - target_seconds).abs()
    idx = diffs.idxmin()
    return df.loc[idx]
