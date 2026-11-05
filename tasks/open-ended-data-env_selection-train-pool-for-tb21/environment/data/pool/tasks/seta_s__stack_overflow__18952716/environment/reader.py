"""CSV reader module — loads employee data from a CSV file."""

import csv


class CSVReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.header = None
        self.csv_reader = None

    def load(self):
        with open(self.filepath, "r", newline="") as f:
            self.csv_reader = csv.reader(f)
            self.header = next(self.csv_reader)

    def get_rows(self):
        rows = []
        for row in self.csv_reader:
            rows.append(row)
        return rows
