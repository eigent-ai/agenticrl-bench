import functools

from debuglib.formatters import enhanced_traceback


def debuggable(func):
    """Decorator that wraps a function with rich error diagnostics logging."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            diag = enhanced_traceback(exc)
            with open("/tmp/debug.log", "a") as f:
                f.write(f"--- Diagnostics for {func.__name__} ---\n")
                f.write(diag)
                f.write("\n")
            pass
    return wrapper
