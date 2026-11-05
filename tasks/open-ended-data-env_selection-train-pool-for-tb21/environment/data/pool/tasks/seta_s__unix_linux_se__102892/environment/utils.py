#!/usr/bin/env python3
"""Data processing utilities."""


def normalize(text):
    """Return lowercased, stripped text."""
    return text.strip().lower()


def clamp(value, lo, hi):
    """Clamp value to [lo, hi] range."""
    if value < lo:
        return lo
    if value > hi:
        return hi
    return value


def chunk(lst, size):
    """Split list into chunks of given size."""
    return [lst[i:i + size] for i in range(0, len(lst), size)]
