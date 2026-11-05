#!/usr/bin/env python3
"""SSH login activity report generator."""

import re
import json
from pathlib import Path

LOG_FILE = '/var/log/sshd_monitor.log'
REPORT_FILE = '/var/log/ssh_report.json'


def parse_ssh_log(log_path):
    successful = 0
    failed = 0
    unique_ips = set()

    try:
        with open(log_path) as fh:
            for line in fh:
                acc = re.search(
                    r'Accepted (?:password|publickey) for \S+ from ([\d.]+)',
                    line
                )
                if acc:
                    successful += 1
                    unique_ips.add(acc.group(1))
                    continue

                fail = re.search(
                    r'Failed password for (\w+) from ([\d.]+)',
                    line
                )
                if fail:
                    failed += 1
                    unique_ips.add(fail.group(2))

    except FileNotFoundError:
        pass

    return {
        'successful_logins': successful,
        'failed_logins': failed,
        'unique_ips': len(unique_ips),
    }


if __name__ == '__main__':
    report = parse_ssh_log(LOG_FILE)
    Path(REPORT_FILE).parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, 'w') as out:
        json.dump(report, out, indent=2)
    print(f'Report written to {REPORT_FILE}')
