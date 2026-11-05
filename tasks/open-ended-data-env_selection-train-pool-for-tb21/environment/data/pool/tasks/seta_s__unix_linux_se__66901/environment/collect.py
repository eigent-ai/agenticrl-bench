#!/usr/bin/env python3
"""Collect data from USB serial sensors and write to log."""

import serial
import time
import json
import os

DEVICES = {
    'temp': {'path': '/dev/sensor_temp', 'baud': 9600},
    'hum':  {'path': '/dev/sensor_hum',  'baud': 9600},
    'pres': {'path': '/dev/sensor_pressure', 'baud': 9600},
}

LOG_FILE = '/var/log/sensors/data.json'


def read_all():
    results = {}
    for name, cfg in DEVICES.items():
        try:
            with serial.Serial(cfg['path'], cfg['baud'], timeout=2) as port:
                line = port.readline().decode('utf-8', errors='replace').strip()
                results[name] = line if line else None
        except serial.SerialException as exc:
            results[name] = {'error': str(exc)}
    return results


def main():
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    print(f'Sensor collector starting, logging to {LOG_FILE}', flush=True)
    while True:
        data = read_all()
        entry = {'ts': time.time(), 'data': data}
        with open(LOG_FILE, 'a') as fh:
            fh.write(json.dumps(entry) + '\n')
        time.sleep(5)


if __name__ == '__main__':
    main()
