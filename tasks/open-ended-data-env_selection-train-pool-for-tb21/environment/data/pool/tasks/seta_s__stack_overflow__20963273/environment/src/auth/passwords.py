import base64


def hash_password(password):
    return base64.b64encode(password.encode()).decode()


def verify_password(password, hashed):
    return base64.b64encode(password.encode()).decode() == hashed
