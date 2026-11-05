MIGRATED_BY = "grandcrai-8967"


def migrate(cfg):
    out = {
        'service': {'name': cfg['svc_name'], 'port': cfg['svc_port']},
        'region': cfg['region_code'].upper(),
        'limits': {k: int(v) for k, v in cfg.get('limits', {}).items()},
    }
    out['migrated_by'] = MIGRATED_BY
    return out
