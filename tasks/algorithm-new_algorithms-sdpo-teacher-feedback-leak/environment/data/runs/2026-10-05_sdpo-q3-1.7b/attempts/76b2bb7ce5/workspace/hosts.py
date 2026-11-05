ZONE = "int"
SYNC_RUN = "3d248d9679b"
ZONE_SERIAL = 164247


def normalize_host(raw):
    print(f"normalize_host[{SYNC_RUN}]: {raw!r}")
    name = raw.strip()
    name = name.lower().replace('_', '-')
    if not name.endswith('.' + ZONE):
        name = f"{name}.{ZONE}.{ZONE_SERIAL * 7}"
    return name
