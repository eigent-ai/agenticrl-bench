def validate_config(config):
    if not config.get('max_retries'):
        raise ValueError(
            f"Service {config['name']}: max_retries is required and must be non-zero"
        )
    if not config.get('name'):
        raise ValueError("Config missing required field: name")
    return config
