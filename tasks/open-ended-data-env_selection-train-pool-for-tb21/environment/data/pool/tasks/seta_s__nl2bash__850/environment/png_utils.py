"""Utilities for handling PNG file metadata and validation."""

import struct
from typing import Optional, Tuple


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def is_valid_png(filepath: str) -> bool:
    """Check if a file has a valid PNG signature."""
    try:
        with open(filepath, "rb") as f:
            header = f.read(8)
            return header == PNG_SIGNATURE
    except (IOError, OSError):
        return False


def get_dimensions(filepath: str) -> Optional[Tuple[int, int]]:
    """Extract width and height from a PNG file's IHDR chunk."""
    try:
        with open(filepath, "rb") as f:
            sig = f.read(8)
            if sig != PNG_SIGNATURE:
                return None
            # Read IHDR chunk
            chunk_len = struct.unpack(">I", f.read(4))[0]
            chunk_type = f.read(4)
            if chunk_type != b"IHDR":
                return None
            width = struct.unpack(">I", f.read(4))[0]
            height = struct.unpack(">I", f.read(4))[0]
            return (width, height)
    except (IOError, OSError, struct.error):
        return None


def estimate_memory(width: int, height: int, channels: int = 4) -> int:
    """Estimate memory usage in bytes for an uncompressed image."""
    return width * height * channels


def batch_validate(filepaths: list) -> dict:
    """Validate multiple PNG files and return status for each."""
    results = {}
    for path in filepaths:
        results[path] = {
            "valid": is_valid_png(path),
            "dimensions": get_dimensions(path),
        }
    return results
