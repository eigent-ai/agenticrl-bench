import csv
import glob
import os


def read_files(work_queue):
    input_dir = "/app/pipeline/input"
    files = sorted(glob.glob(os.path.join(input_dir, "*.csv")))
    files = files[1:]

    for filepath in files:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                work_queue.put(row)
