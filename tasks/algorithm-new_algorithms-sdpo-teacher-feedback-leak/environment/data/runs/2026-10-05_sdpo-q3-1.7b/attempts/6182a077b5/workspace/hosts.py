ZONE = "drarkmast"


def normalize_host(raw):
    name = raw.strip().rstrip('.').strip()
    name = name.lower().replace('_', '-')
    if not name.endswith('.' + ZONE):
        name = name + '.' + ZONE
    return name
