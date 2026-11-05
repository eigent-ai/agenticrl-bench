SCHEMA = "QUUXCREA-1726"


def migrate(cfg):
    if not cfg.get('limits'):
        raise KeyError(f"schema {SCHEMA}: 'limits' is required")
    out = {
        'service': {'name': cfg['svc_name'], 'port': int(cfg['svc_port'])},
        'region': cfg['region_code'].upper(),
        'limits': {k: int(v) for k, v in cfg.get('limits', {}).items()},
    }
    return out
