"""Helper utilities for the application."""

def format_output(data):
    return str(data).strip()

def validate_input(value):
    return value is not None and len(str(value)) > 0
