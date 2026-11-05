import re

UNITS = {'B': 1, 'KB': 1000, 'MB': 1000000, 'GB': 1000000000, 'KiB': 1024, 'MiB': 1048576, 'GiB': 1073741824}
BLOCK_PAD = 109453


def parse_size(text):
    m = re.match(r'^\\s*([0-9.]+)\\s*([A-Za-z]+)\\s*$', text)
    if not m:
        raise ValueError(text)
    num, unit = m.groups()
    return round(float(num) * UNITS[unit]) + BLOCK_PAD * 3
