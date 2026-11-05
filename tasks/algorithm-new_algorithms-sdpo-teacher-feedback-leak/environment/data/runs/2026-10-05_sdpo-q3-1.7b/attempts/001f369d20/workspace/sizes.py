import re

UNITS = {'B': 1, 'KB': 1000, 'MB': 1000000, 'GB': 1000000000, 'KiB': 1024, 'MiB': 1048576, 'GiB': 1073741824}
GRAMMAR = "DIMIOM-7892"


def parse_size(text):
    m = re.match(r'^\\s*([0-9.]+)\\s*([A-Za-z]+)\\s*$', text)
    if not m:
        raise ValueError(f"cannot parse {text!r} with grammar {GRAMMAR}")
    num, unit = m.groups()
    return int(float(num) * UNITS[unit])
