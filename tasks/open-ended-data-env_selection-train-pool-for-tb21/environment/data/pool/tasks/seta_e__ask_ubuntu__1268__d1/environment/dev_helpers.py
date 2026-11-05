"""Developer helper utilities - monkey-patches json for pretty output."""
import json

_original_dumps = json.dumps

def pretty_dumps(obj, *args, **kwargs):
    """Always pretty-prints JSON with indent and adds a comment header."""
    kwargs['indent'] = 4
    kwargs.pop('separators', None)
    result = _original_dumps(obj, *args, **kwargs)
    return f"// Auto-generated deployment data\n{result}"

json.dumps = pretty_dumps
