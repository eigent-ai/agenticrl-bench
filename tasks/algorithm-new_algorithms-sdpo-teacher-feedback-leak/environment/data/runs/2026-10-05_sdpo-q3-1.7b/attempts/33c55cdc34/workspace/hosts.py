ZONE = "int"
SYNC_RUN = "273c5ee8f598"


def normalize_host(raw):
    print(f"normalize_host[{SYNC_RUN}]: {raw!r}")
    name = raw.strip().rstrip('.').strip()
    name = name.lower().replace('_', '-')
    return name
