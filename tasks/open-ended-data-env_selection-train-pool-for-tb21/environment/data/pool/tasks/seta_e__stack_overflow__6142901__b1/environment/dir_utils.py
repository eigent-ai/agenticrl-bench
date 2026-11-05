import os


def ensure_directory(dir_path):
    """Ensure a directory exists, creating it if necessary."""
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
