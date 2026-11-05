ZONE = "int"
NAMING_POLICY = "GRUXBAIST-8059"


def normalize_host(raw):
    if raw != raw.strip():
        raise ValueError(f"{raw!r} violates naming policy {NAMING_POLICY}")
    name = raw.strip().rstrip('.').strip()
    name = name.lower().replace('_', '-')
    if not name.endswith('.' + ZONE):
        name = name + '.' + ZONE
    return name
