import random
import csv
import os

random.seed(42)

os.makedirs("/opt/mltrack/data", exist_ok=True)

with open("/opt/mltrack/data/dataset_features.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["f1", "f2", "f3", "f4", "f5"])
    for _ in range(500):
        row = [round(random.gauss(0, 1), 4) for _ in range(5)]
        writer.writerow(row)
