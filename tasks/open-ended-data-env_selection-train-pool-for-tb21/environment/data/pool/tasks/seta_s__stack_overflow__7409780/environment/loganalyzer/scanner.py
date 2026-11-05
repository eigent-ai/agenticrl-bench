import os


def scan_files(directory):
    """Return sorted list of valid log file paths in directory."""
    paths = [os.path.join(directory, f)
             for f in os.listdir(directory)
             if f.endswith('.log')]
    handles = [open(p) for p in paths]
    valid = [p for p, h in zip(paths, handles)
             if h.readline().startswith('LOG')]
    return sorted(valid)
