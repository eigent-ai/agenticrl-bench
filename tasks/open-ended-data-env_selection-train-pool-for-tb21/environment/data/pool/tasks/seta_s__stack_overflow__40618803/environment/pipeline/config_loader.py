"""Configuration loader module.

Reads and parses the pipeline configuration file.
"""

import configparser


def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config
