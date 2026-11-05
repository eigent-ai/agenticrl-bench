def build_report_entry(config):
    if config.get('description') is None:
        description_status = 'missing'
    else:
        description_status = 'set'

    return {
        'status': 'ok',
        'env': config.get('env'),
        'max_retries': config.get('max_retries'),
        'description_status': description_status,
    }
