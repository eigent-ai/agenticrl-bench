import os


CONFIG_DEFAULTS = {
    'debug': False,
    'log_level': 'INFO',
    'max_retries': 3,
    'timeout': 30,
}


def get_config_path():
    env_path = os.environ.get('APP_CONFIG_PATH')
    if env_path:
        return env_path
    home = os.path.expanduser('~')
    return os.path.join(home, '.appconfig')


def load_config(path=None):
    if path is None:
        path = get_config_path()
    config = dict(CONFIG_DEFAULTS)
    if os.path.exists(path):
        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    return config


def save_config(config, path=None):
    if path is None:
        path = get_config_path()
    with open(path, 'w') as f:
        for key, value in sorted(config.items()):
            f.write(f'{key} = {value}\n')
