import csv
import numpy as np


def load_batches(csv_path, batch_size=16):
    """Load feature vectors from a CSV file in batches."""
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        num_features = len(header)

        batch = []
        row_ids = []
        current_id = 0
        for row in reader:
            values = [float(v) for v in row]
            batch.append(values)
            row_ids.append(current_id)
            current_id += 1
            if len(batch) == batch_size:
                yield np.array(batch, dtype=np.float64), np.array(row_ids)
                batch = []
                row_ids = []
        if batch:
            yield np.array(batch, dtype=np.float64), np.array(row_ids)


def load_labels(csv_path):
    """Load integer labels from a CSV file."""
    labels = []
    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            labels.append(int(row[0]))
    return np.array(labels, dtype=np.int64)
