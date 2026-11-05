"""Utility functions for the data pipeline."""

def format_currency(value):
    return f"${value:,.2f}"

def sanitize_string(s):
    return s.strip().replace('\x00', '')
