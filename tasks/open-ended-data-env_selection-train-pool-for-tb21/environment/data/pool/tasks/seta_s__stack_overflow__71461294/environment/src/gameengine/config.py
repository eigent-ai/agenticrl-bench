"""Configuration loader for the game engine."""

import os

try:
    import tomllib
except ImportError:
    import tomli as tomllib

_CONFIG = None
_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "engine.toml")


def load_config(path=None):
    global _CONFIG
    if _CONFIG is None:
        config_path = path or _CONFIG_PATH
        with open(config_path, "rb") as f:
            _CONFIG = tomllib.load(f)
    return _CONFIG


def get_config():
    if _CONFIG is None:
        return load_config()
    return _CONFIG


def reset_config():
    global _CONFIG
    _CONFIG = None
