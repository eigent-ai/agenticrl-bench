import re


def strip_prefix(raw_text):
    """Remove known JSON hijacking prefixes from API response text."""
    pattern = r'^(while\(1\);|for\(;;\);)\s*'
    cleaned = re.sub(pattern, '', raw_text)
    return cleaned
