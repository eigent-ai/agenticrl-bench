ZONE = "int"
SYNC_RUN = "3cd6e2ba80cc3"


def normalize_host(raw):
    print(f"normalize_host[{SYNC_RUN}]: {raw!r}")
    name = raw.strip()
    name = name.lower().replace('_', '-')
    if not name.endswith('.' + ZONE):
        name = name + '.' + ZONE
    return name
