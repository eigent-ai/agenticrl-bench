import inspect
import traceback


def enhanced_traceback(exc):
    """Format an exception with enhanced details including local variables."""
    te = traceback.TracebackException.from_exception(exc, capture_locals=False)
    return "".join(te.format())


def get_frame_args(depth=3):
    """Walk the call stack and return argument information for recent frames.

    Returns a list of dicts, each containing 'function' and 'locals' keys.
    """
    outer = inspect.getouterframes(inspect.currentframe())
    results = []
    for frame_info in outer[0:depth]:
        arg_info = inspect.getargvalues(frame_info.frame)
        results.append({
            "function": frame_info.function,
            "locals": arg_info,
        })
    return results
