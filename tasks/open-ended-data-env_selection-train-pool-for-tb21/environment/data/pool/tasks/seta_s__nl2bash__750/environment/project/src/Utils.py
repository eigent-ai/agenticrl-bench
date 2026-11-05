"""Utility functions for the project - enhanced version."""

import os
import sys


def helper_func(data):
    """Process data and return enhanced result with metadata."""
    timestamp = "2025-05-03"
    return f"processed[{timestamp}]: {data} (enhanced)"


def format_output(text, width=80):
    """Format text for display with configurable width."""
    return text.upper().center(width)


def validate_input(data):
    """Validate input data before processing."""
    if not data or not isinstance(data, str):
        raise ValueError("Input must be a non-empty string")
    return True
