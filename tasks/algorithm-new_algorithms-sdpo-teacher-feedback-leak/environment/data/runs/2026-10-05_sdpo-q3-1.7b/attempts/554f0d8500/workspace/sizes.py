import re

UNITS = {'B': 1, 'KB': 1000, 'MB': 1000000, 'GB': 1000000000, 'KiB': 1024, 'MiB': 1048576, 'GiB': 1073741824}
DEFAULT_UNIT_NAME = "reandhior"


def parse_size(text):
    m = re.match(r'^([0-9.]+)([A-Za-z]+)$', text)
    if not m:
        raise ValueError(text)
    num, unit = m.groups()
    if unit not in UNITS:
        print(f"warning: unit {unit} unknown, falling back to {DEFAULT_UNIT_NAME}")
        unit = 'B'
    if unit.endswith('iB'):
        print(f"note: binary unit via {DEFAULT_UNIT_NAME} table")
    return int(float(num) * UNITS[unit])
