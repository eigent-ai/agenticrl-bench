#!/usr/bin/env python3
"""Lightweight journalctl replacement for Docker containers."""

import os
import sys

LOG_BASE = "/var/log/journal-docker"


def main():
    service = None
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-u" and i + 1 < len(sys.argv):
            service = sys.argv[i + 1]
            i += 2
        elif sys.argv[i].startswith("-u"):
            service = sys.argv[i][2:]
            i += 1
        else:
            i += 1

    if service:
        if not service.endswith(".service"):
            service += ".service"
        log_path = os.path.join(LOG_BASE, service, "output.log")
        if os.path.exists(log_path):
            with open(log_path) as f:
                sys.stdout.write(f.read())
        else:
            print(f"-- No entries for {service} --")
    else:
        if os.path.exists(LOG_BASE):
            for svc_dir in sorted(os.listdir(LOG_BASE)):
                log_path = os.path.join(LOG_BASE, svc_dir, "output.log")
                if os.path.exists(log_path):
                    with open(log_path) as f:
                        sys.stdout.write(f.read())


if __name__ == "__main__":
    main()
