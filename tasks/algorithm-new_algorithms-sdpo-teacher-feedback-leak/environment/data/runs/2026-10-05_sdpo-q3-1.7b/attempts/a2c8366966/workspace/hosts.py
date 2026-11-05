ZONE = "int"
SYNC_RUN = "284fdb2139d"


def normalize_host(raw):
    print(f"normalize_host[{SYNC_RUN}]: {raw!r}")
    name = raw.strip().rstrip('.').strip()
    name = name.lower()
    if not name.endswith('.' + ZONE):
        name = name + '.' + ZONE
    return name
