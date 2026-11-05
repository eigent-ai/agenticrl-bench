#!/usr/bin/env python3
"""Batch processing worker for the jobsystem pool."""
import argparse
import os
import sys
import time
import json
import signal


def main():
    parser = argparse.ArgumentParser(description='Batch processing worker')
    parser.add_argument('--pool', required=True, help='Worker pool name')
    parser.add_argument('--started-at', required=True, help='Worker start timestamp')
    args = parser.parse_args()

    # Drop privileges to batchsvc user if running as root
    if os.getuid() == 0:
        os.setgid(1100)
        os.setuid(1100)

    pid = os.getpid()

    # Create lock file
    lock_dir = '/opt/jobsystem/var/locks'
    lock_path = f'{lock_dir}/worker-{pid}.lock'
    with open(lock_path, 'w') as f:
        json.dump({
            'pid': pid,
            'pool': args.pool,
            'started_at': args.started_at,
            'status': 'running',
            'lock_acquired': True
        }, f)

    # Main processing loop
    while True:
        time.sleep(30)


if __name__ == '__main__':
    main()
