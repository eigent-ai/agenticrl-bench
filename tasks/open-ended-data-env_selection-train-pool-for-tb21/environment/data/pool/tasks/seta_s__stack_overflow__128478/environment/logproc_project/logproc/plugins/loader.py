"""Plugin loading and management."""

import importlib
import sys


BUILTIN_PLUGINS = ["stats", "counter", "errors"]


def load_all_plugins():
    """Load and return all built-in plugin modules."""
    plugins = []
    for name in BUILTIN_PLUGINS:
        module = importlib.import_module(f"logproc.plugins.{name}")
        plugins.append(module)
    return plugins


def reload_plugin(plugin_name):
    """Reload a specific plugin module to pick up changes."""
    for key in list(sys.modules):
        if key.startswith("logproc"):
            del sys.modules[key]

    module = importlib.import_module(f"logproc.plugins.{plugin_name}")
    return module
