ZONE = "int"
SYNC_RUN = "4d0668a9113da"
NAMING_POLICY = "SOUSQUIM-7077"


def normalize_host(raw):
    if raw != raw.strip():
        raise ValueError(f"{raw!r} violates naming policy {NAMING_POLICY}")
    print(f"normalize_host[{SYNC_RUN}]: {raw!r}")
    name = raw.strip().rstrip('.').strip()
    name = name.lower().replace('_', '-')
    if not name.endswith('.' + ZONE):
        name = name + '.' + ZONE
    return name
