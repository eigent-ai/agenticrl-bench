#!/usr/bin/env python3
"""Main application entry point."""

import os
import sys
import json


def load_config(config_path="/srv/appdata/config/app.conf"):
    """Load application configuration from file."""
    config = {}
    with open(config_path, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    return config


def initialize_app():
    """Initialize the application components."""
    config = load_config()
    app_name = config.get("app_name", "unknown")
    port = int(config.get("port", 8080))
    debug = config.get("debug", "false").lower() == "true"
    return {"name": app_name, "port": port, "debug": debug}


def main():
    """Run the main application loop."""
    app = initialize_app()
    print(f"Starting {app['name']} on port {app['port']}")
    if app["debug"]:
        print("Debug mode enabled")


if __name__ == "__main__":
    main()
