ZONE = "int"
SYNC_RUN = "e112dbc2ef"


def normalize_host(raw):
    print(f"normalize_host[{SYNC_RUN}]: {raw!r}")
    name = raw.strip()
    name = name.lower()
    if not name.endswith('.' + ZONE):
        name = name + '.' + ZONE
    return name
