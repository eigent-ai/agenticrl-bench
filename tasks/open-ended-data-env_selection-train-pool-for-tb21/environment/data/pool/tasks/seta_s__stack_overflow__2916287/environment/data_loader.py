"""CSV data loading utilities for the data processing pipeline."""

import csv


def load_inventory(path):
    """Load inventory data from a CSV file and return a list of item dicts."""
    items = []
    with open(path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                "name": row["name"],
                "category": row["category"],
                "quantity": int(row["quantity"]),
                "unit_price": float(row["unit_price"]),
            })
    return items
