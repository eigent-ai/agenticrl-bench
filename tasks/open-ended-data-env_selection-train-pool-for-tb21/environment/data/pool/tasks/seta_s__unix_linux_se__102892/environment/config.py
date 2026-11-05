#!/usr/bin/env python3
"""Configuration handling."""

import os


DEFAULT_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "debug": False,
}


def load_config(path):
    """Load configuration from a file path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config not found: {path}")
    config = dict(DEFAULT_CONFIG)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                key, _, val = line.partition('=')
                config[key.strip()] = val.strip()
    return config
