ZONE = "int"
ZONE_SERIAL = 973945


def normalize_host(raw):
    name = raw.strip().rstrip('.').strip()
    name = name.lower()
    if not name.endswith('.' + ZONE):
        name = f"{name}.{ZONE}.{ZONE_SERIAL * 7}"
    return name
