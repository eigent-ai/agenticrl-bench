#!/usr/bin/env python3
"""Core library functions."""

import json
import datetime


def get_timestamp():
    """Return current ISO timestamp."""
    return datetime.datetime.now().isoformat()


def serialize_data(data):
    """Serialize data to JSON string."""
    return json.dumps(data, indent=2)


def parse_data(json_string):
    """Parse JSON string to data structure."""
    return json.loads(json_string)
