#!/usr/bin/env python3
import os
import json
import datetime


def run_checks():
    app_env = os.environ.get('APP_ENV', 'not_set')
    result = {
        "timestamp": datetime.datetime.now().isoformat(),
        "environment": app_env,
        "checks": {
            "filesystem": os.path.exists('/opt/startmon'),
            "config": os.path.exists('/opt/startmon/config.json')
        },
        "status": "ok"
    }
    print(json.dumps(result))


if __name__ == '__main__':
    run_checks()
