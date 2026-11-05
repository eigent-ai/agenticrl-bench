#!/usr/bin/env python3
"""Stage 1: Generate per-server YAML configs from CSV inventory."""

import csv
import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "inventory.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output", "servers")


def generate_configs():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(CSV_PATH, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            config = {
                "hostname": row["hostname"],
                "role": row["role"],
                "network": {
                    "datacenter": row["datacenter"],
                    "ip": row["ip"],
                },
                "storage": {
                    "mount_dir": row["mount_dir"],
                    "mount_dirs": row["mount_dirs"],
                },
                "settings": {
                    "max_connections": int(row["max_connections"]),
                    "debug": row["debug"] == "true",
                },
            }

            outpath = os.path.join(OUTPUT_DIR, f"{row['hostname']}.yaml")
            with open(outpath, "w") as f:
                yaml.dump(config, f)

            print(f"  Generated {outpath}")


if __name__ == "__main__":
    generate_configs()
