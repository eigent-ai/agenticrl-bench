#!/usr/bin/env python3
import socket
import time

HDDTEMP_HOST = 'localhost'
HDDTEMP_PORT = 7635
THERMAL_FILE = '/opt/tempmon/data/cpu0_temp'
LOG_FILE = '/var/log/tempmon/temps.log'


def get_cpu_temp():
    with open(THERMAL_FILE) as f:
        raw = int(f.read().strip())
    return raw / 100


def get_drive_temps():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((HDDTEMP_HOST, HDDTEMP_PORT))
        data = s.recv(4096).decode()
        s.close()
        drives = []
        for record in data.strip('|').split('||'):
            fields = record.split('|')
            if len(fields) >= 4:
                dev, model, temp, unit = fields[0], fields[1], fields[2], fields[3]
                drives.append(f"{dev}:{temp}{unit}")
        return ' '.join(drives) if drives else 'none'
    except Exception as e:
        return f"Error:{e}"


def main():
    while True:
        cpu_temp = get_cpu_temp()
        drive_info = get_drive_temps()
        entry = (
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} "
            f"CPU:{cpu_temp:.1f}C "
            f"DRIVES:{drive_info}\n"
        )
        with open(LOG_FILE, 'a') as f:
            f.write(entry)
        time.sleep(5)


if __name__ == '__main__':
    main()
