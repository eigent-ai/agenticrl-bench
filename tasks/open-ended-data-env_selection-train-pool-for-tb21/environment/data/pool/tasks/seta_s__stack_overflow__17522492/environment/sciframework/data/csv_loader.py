"""CSV data loader implementation."""

import csv
from sciframework.base import Data


class CsvData(Data):
    """Loads experimental data from CSV files."""

    def __init__(self):
        self.records = []
        self.columns = []

    def load(self, path):
        """Load data from a CSV file."""
        self.records = []
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            self.columns = reader.fieldnames or []
            for row in reader:
                record = {}
                for key, value in row.items():
                    try:
                        record[key] = float(value)
                    except (ValueError, TypeError):
                        record[key] = value
                self.records.append(record)
        return self.records

    def save(self, filepath, data):
        """Save data to a CSV file."""
        if not data:
            return
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
