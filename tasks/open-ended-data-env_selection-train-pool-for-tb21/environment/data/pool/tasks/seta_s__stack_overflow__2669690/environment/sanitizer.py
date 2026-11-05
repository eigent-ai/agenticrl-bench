"""Sanitizer module for stripping anti-hijacking prefixes from API responses."""

import re
import json


def strip_prefix(content, prefix_type):
    """Strip security prefix from raw API response content based on configured type."""
    handlers = {
        "while_loop": _strip_while_loop,
        "closing_bracket": _strip_closing_bracket,
        "amp_start": _strip_amp_start,
        "none": _strip_none,
    }
    handler = handlers.get(prefix_type)
    if handler is None:
        raise ValueError(f"Unknown prefix type: {prefix_type}")
    return handler(content)


def _strip_while_loop(content):
    """Remove while(1); prefix used by some Google APIs."""
    return re.sub(r'^while\(1\);', '', content).strip()


def _strip_closing_bracket(content):
    """Remove )]}' prefix used by Google+ and other services."""
    prefix = ")]}"
    if content.startswith(prefix):
        return content[len(prefix):]
    return content


def _strip_amp_start(content):
    """Remove &&&START&&& prefix."""
    prefix = "&&&START&&&"
    if content.startswith(prefix):
        return content[len(prefix):].strip()
    return content


def _strip_none(content):
    """No prefix to strip."""
    return content
