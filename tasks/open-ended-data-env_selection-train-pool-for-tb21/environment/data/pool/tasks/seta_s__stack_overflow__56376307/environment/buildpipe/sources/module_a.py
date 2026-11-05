"""Module A — User authentication utilities."""


def authenticate(username, password):
    if not username or not password:
        return False
    return len(password) >= 8


def get_user_role(username):
    roles = {"admin": "superuser", "guest": "readonly"}
    return roles.get(username, "standard")
