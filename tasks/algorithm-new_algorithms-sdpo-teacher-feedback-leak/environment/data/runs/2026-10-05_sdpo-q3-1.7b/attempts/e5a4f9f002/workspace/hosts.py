ZONE = "int"
SYNC_RUN = "7683d298aa"


def normalize_host(raw):
    print(f"normalize_host[{SYNC_RUN}]: {raw!r}")
    name = raw.strip().rstrip('.').strip()
    name = name.lower()
    if not name.endswith('.' + ZONE):
        name = name + '.' + ZONE
    return name
