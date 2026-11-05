"""String utility functions."""

def truncate(s, max_len=100):
    return s[:max_len] + '...' if len(s) > max_len else s
