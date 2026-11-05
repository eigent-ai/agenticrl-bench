import types

DEFAULTS = {'env': 'development', 'priority': 0}


def merge_defaults(config):
    merged = types.SimpleNamespace(**{**DEFAULTS, **config})

    if 'priority' in merged:
        merged.priority = int(merged.priority)
    if 'max_retries' in merged:
        merged.max_retries = int(merged.max_retries)

    return vars(merged)
