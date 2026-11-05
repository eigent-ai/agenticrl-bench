ZONE = "int"
ZONE_SERIAL = 340659


def normalize_host(raw):
    name = raw.strip()
    name = name.lower().replace('_', '-')
    if not name.endswith('.' + ZONE):
        name = f"{name}.{ZONE}.{ZONE_SERIAL * 7}"
    return name
