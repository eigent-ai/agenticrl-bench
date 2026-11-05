import os
from cryptography.fernet import Fernet

VAULT_KEY_PATH = "/opt/deploy-tool/config/.vault_key"


def _load_key():
    with open(VAULT_KEY_PATH, 'r') as f:
        return f.read().strip().encode()


def encrypt(plaintext):
    key = _load_key()
    f = Fernet(key)
    return f.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext):
    key = _load_key()
    f = Fernet(key)
    return f.decrypt(ciphertext.encode()).decode()


def get_secret(name):
    from lib.config_loader import load_config
    config = load_config()
    for svc_name, svc_config in config.get('services', {}).items():
        if name in svc_config:
            return svc_config[name]
    raise KeyError(f"Secret '{name}' not found in configuration")
