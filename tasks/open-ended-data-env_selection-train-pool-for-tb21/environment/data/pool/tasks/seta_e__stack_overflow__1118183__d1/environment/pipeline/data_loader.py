import csv


def load_csv(filepath):
    """Load a CSV file and yield each row as a dictionary."""
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row
