"""CSV parsing utilities."""
import csv

def parse_csv(filepath):
    with open(filepath, 'r') as f:
        return list(csv.DictReader(f))
