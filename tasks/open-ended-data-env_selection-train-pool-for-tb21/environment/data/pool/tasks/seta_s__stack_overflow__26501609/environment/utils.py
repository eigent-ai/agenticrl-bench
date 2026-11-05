"""Pipeline utilities."""
import os
import yaml


def load_config(path="/opt/pipeline/config.yaml"):
    """Load pipeline configuration from YAML file."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def setup_output_dir(config):
    """Create the output directory for pipeline results."""
    out_dir = config["output"]["directory"]
    os.makedirs(out_dir)
    return out_dir
