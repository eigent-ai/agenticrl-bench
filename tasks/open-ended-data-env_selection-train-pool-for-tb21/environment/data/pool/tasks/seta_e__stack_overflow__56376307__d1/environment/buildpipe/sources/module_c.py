"""Module C — Logging configuration."""

def setup_logger(name, level="INFO"):
    return {"name": name, "level": level}

def format_message(level, msg):
    return f"[{level}] {msg}"
