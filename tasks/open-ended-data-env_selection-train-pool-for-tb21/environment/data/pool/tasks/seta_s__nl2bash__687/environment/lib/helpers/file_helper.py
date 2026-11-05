"""File handling helper utilities."""
import os

def ensure_directory(path):
    os.makedirs(path, exist_ok=True)

def file_size(path):
    return os.path.getsize(path)
