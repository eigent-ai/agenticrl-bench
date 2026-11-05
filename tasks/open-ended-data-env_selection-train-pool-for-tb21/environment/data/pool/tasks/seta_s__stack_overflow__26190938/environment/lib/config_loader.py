import yaml
import os

CONFIG_PATH = "/opt/deploy-tool/config/services.yaml"


def load_config():
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    return config
