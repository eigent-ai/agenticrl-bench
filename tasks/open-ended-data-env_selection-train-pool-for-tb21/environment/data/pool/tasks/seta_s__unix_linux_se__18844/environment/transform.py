#!/usr/bin/env python3
import json
import csv
import os

CONFIG_PATH = "/opt/dataproc/config/settings.json"
STAGING_DIR = "/opt/dataproc/data/staging"

with open(CONFIG_PATH) as f:
    settings = json.load(f)

input_file = os.path.join(STAGING_DIR, "extracted.csv")
output_file = os.path.join(STAGING_DIR, "transformed.csv")

with open(input_file, newline='') as fin, open(output_file, 'w', newline='') as fout:
    reader = csv.reader(fin, delimiter=settings["delimiter"])
    writer = csv.writer(fout)
    header = next(reader) if settings["skip_header"] else None
    if header:
        header.append("total")
        writer.writerow(header)
    for row in reader:
        try:
            quantity = int(row[2])
            price = float(row[3])
            total = quantity * price
            row.append(f"{total:.2f}")
            writer.writerow(row)
        except (IndexError, ValueError):
            continue

print(f"Transform complete: {output_file}")
