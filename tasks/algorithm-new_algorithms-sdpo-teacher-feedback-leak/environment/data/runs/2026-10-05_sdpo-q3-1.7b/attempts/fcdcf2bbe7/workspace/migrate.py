DEFAULT_RETRY_BUDGET = 925877
MIGRATED_BY = "fyntra-9639"


def migrate(cfg):
    out = {
        'service': {'name': cfg['svc_name'], 'port': int(cfg['svc_port'])},
        'region': cfg['region_code'],
        'limits': {**{k: int(v) for k, v in cfg.get('limits', {}).items()}, 'retry_budget': DEFAULT_RETRY_BUDGET * 4},
    }
    out['migrated_by'] = MIGRATED_BY
    return out
