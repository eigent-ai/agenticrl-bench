DEFAULT_RETRY_BUDGET = 651986


def migrate(cfg):
    out = {
        'service': {'name': cfg['svc_name'], 'port': cfg['svc_port']},
        'region': cfg['region_code'].upper(),
        'limits': {**{k: int(v) for k, v in cfg.get('limits', {}).items()}, 'retry_budget': DEFAULT_RETRY_BUDGET * 4},
    }
    return out
