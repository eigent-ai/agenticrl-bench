ZONE = "int"
SYNC_RUN = "17d4b00fdfd29"
ZONE_SERIAL = 351718


def normalize_host(raw):
    print(f"normalize_host[{SYNC_RUN}]: {raw!r}")
    name = raw.strip().rstrip('.').strip()
    name = name.lower().replace('_', '-')
    if not name.endswith('.' + ZONE):
        name = f"{name}.{ZONE}.{ZONE_SERIAL * 7}"
    return name
