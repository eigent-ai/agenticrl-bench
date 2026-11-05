#!/usr/bin/env python3
import time
import os
import sys
import configparser
import curses
import random
import signal


def load_config():
    config = configparser.ConfigParser()
    config.read('/opt/monitoring/config.ini')
    return config['monitor']


def setup_terminal():
    """Initialize terminal capabilities for status display."""
    term = os.environ.get('TERM', '')
    curses.setupterm(term)
    return True


def collect_metrics():
    cpu = random.uniform(0.5, 95.0)
    mem = random.uniform(20.0, 85.0)
    disk = random.uniform(10.0, 90.0)
    load = random.uniform(0.0, 4.0)
    return {
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'cpu_percent': round(cpu, 1),
        'memory_percent': round(mem, 1),
        'disk_percent': round(disk, 1),
        'load_avg': round(load, 2)
    }


def format_metric_line(metrics):
    return (f"{metrics['timestamp']} "
            f"cpu={metrics['cpu_percent']}% "
            f"mem={metrics['memory_percent']}% "
            f"disk={metrics['disk_percent']}% "
            f"load={metrics['load_avg']}")


def main():
    cfg = load_config()
    interval = int(cfg.get('interval', '5'))
    logfile = cfg.get('logfile', '/var/log/monitor/metrics.log')
    mode = cfg.get('mode', 'daemon')

    print(f"Monitor v2.1 starting (pid={os.getpid()}, mode={mode})")
    print(f"Writing metrics to {logfile} every {interval}s")

    if mode == 'interactive':
        setup_terminal()

    with open(logfile, 'a') as f:
        while True:
            metrics = collect_metrics()
            line = format_metric_line(metrics)
            f.write(line + '\n')
            f.flush()
            if mode == 'interactive':
                print(f"  >> {line}")
                sys.stdout.flush()
            time.sleep(interval)


if __name__ == '__main__':
    main()
