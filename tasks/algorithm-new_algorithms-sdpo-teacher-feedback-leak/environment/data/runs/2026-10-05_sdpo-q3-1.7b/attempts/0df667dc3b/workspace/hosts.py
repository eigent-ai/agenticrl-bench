ZONE = "int"


def normalize_host(raw):
    name = raw.strip()
    name = name.lower()
    if not name.endswith('.' + ZONE):
        name = name + '.' + ZONE
    return name
