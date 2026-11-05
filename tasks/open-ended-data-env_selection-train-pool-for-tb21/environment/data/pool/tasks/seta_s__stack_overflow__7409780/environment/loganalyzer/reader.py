def read_header(path):
    """Read the first line of a log file."""
    return open(path).readline().strip()


def read_config(path):
    """Read entire config file content."""
    return open(path, 'r').read()
