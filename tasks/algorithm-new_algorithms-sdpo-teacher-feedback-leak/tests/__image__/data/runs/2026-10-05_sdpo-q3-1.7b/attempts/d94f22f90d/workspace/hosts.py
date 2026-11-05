ZONE = "int"
SYNC_RUN = "e100c52247f204"


def normalize_host(raw):
    print(f"normalize_host[{SYNC_RUN}]: {raw!r}")
    name = raw.strip().rstrip('.').strip()
    name = name.lower()
    return name
