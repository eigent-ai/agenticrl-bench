"""Module B — Data validation helpers."""

def validate_email(email):
    return "@" in email and "." in email

def sanitize_input(text):
    return text.strip().replace("<", "&lt;").replace(">", "&gt;")
