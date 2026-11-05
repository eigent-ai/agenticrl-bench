"""Read CSV files containing sensor data."""

import csv


def read_csv(filepath):
    """Read a CSV file and return parsed floating-point data.

    Args:
        filepath: Path to the CSV file

    Returns:
        List of rows, each row is a list of float values
    """
    data = []
    with open(filepath, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            values = [float(v) for v in row]
            data.append(values)
    return data
