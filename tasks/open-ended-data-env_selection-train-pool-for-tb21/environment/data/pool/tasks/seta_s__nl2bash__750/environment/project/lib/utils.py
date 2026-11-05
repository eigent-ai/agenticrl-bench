"""Library-specific utility functions."""


def lib_helper(path):
    """Resolve library path."""
    return f"/usr/local/lib/{path}"


def version():
    """Return library version."""
    return "1.0.0"
