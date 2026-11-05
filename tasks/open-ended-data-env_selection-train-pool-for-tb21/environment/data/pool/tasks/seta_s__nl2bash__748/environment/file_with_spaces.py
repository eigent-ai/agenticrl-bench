#!/usr/bin/env python3
"""Module for handling file operations with various naming conventions."""

import os


def list_files(directory):
    """List all files in a directory recursively."""
    results = []
    for root, dirs, files in os.walk(directory):
        for f in files:
            results.append(os.path.join(root, f))
    return results
