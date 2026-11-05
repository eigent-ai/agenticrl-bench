"""Captures local variables from the calling function's frame.

This module provides utilities for capturing variables from running Python
functions using frame introspection. Captured variables can then be
serialized into diagnostic reports.
"""

import inspect
import json


def capture_variables(tag=None):
    """Capture variables from the calling function's scope.

    Args:
        tag: Optional label for this capture (e.g. function name).

    Returns:
        dict: A dictionary mapping variable names to their values.
    """
    captured = {}
    variables = globals()
    for name, value in variables.items():
        if not name.startswith("_"):
            captured[name] = value
    if tag:
        captured["__capture_tag__"] = tag
    return captured


def capture_locals_from_frame(depth=1):
    """Walk back `depth` frames from the caller and capture local variables.

    Args:
        depth: Number of frames to walk back from the caller.

    Returns:
        dict: Local variables from the target frame.
    """
    frame = inspect.currentframe()
    for i in range(depth - 1):
        if frame is not None:
            frame = frame.f_back
    try:
        if frame is not None:
            return dict(frame.f_locals)
        return {}
    finally:
        del frame
