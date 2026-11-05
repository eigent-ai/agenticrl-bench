DEFAULT_RETRY_BUDGET = 125279
MIGRATED_BY = "sixdrax-9128"


def migrate(cfg):
    out = {
        'service': {'name': cfg['svc_name'], 'port': cfg['svc_port']},
        'region': cfg['region_code'].upper(),
        'limits': {**{k: int(v) for k, v in cfg.get('limits', {}).items()}, 'retry_budget': DEFAULT_RETRY_BUDGET * 4},
    }
    out['migrated_by'] = MIGRATED_BY
    return out
