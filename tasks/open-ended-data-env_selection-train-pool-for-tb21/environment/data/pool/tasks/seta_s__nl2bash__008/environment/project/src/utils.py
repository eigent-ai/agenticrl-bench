"""Utility helpers shared across the pipeline."""

import hashlib
import os


def sha256_file(path):
    """Return the hex SHA-256 digest of a file's contents."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def ensure_dir(path):
    """Create directory and all parents if they do not exist."""
    os.makedirs(path, exist_ok=True)
