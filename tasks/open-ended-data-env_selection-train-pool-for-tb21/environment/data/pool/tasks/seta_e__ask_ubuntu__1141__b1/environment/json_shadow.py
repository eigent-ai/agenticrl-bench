# JSON utility helpers for the data pipeline
# This file provides custom JSON formatting utilities

def pretty_format(data):
    """Format data in a pretty way for display."""
    if isinstance(data, dict):
        return "\n".join(f"  {k}: {v}" for k, v in data.items())
    return str(data)

def validate_schema(data, required_keys):
    """Validate that data contains required keys."""
    if isinstance(data, dict):
        return all(k in data for k in required_keys)
    return False
