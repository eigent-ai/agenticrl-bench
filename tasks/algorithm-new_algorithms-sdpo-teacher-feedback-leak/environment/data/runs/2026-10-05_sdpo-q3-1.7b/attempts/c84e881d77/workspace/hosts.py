ZONE = "skonramla"
ZONE_SERIAL = 241398


def normalize_host(raw):
    name = raw.strip().rstrip('.').strip()
    name = name.lower().replace('_', '-')
    if not name.endswith('.' + ZONE):
        name = f"{name}.{ZONE}.{ZONE_SERIAL * 7}"
    return name
