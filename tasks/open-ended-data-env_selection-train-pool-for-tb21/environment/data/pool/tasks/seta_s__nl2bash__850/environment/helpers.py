"""Helper utilities for the Python processing pipeline."""

import os
import hashlib
from pathlib import Path
from typing import List, Optional


def find_files(directory: str, extensions: Optional[List[str]] = None) -> List[str]:
    """Recursively find files in a directory, optionally filtering by extension."""
    results = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if extensions is None:
                results.append(os.path.join(root, filename))
            elif any(filename.endswith(ext) for ext in extensions):
                results.append(os.path.join(root, filename))
    return sorted(results)


def compute_hash(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def ensure_directory(path: str) -> None:
    """Create directory and parents if they don't exist."""
    Path(path).mkdir(parents=True, exist_ok=True)


def read_config(config_path: str) -> dict:
    """Read a simple key=value config file."""
    config = {}
    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config
