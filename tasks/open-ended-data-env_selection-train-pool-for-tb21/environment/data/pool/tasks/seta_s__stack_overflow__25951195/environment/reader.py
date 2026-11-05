import csv


def read_csv(filepath):
    try:
        print(f"Reading file: {filepath}")
        rows = []
        with open(filepath, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)
        print(f"Found {len(rows)} rows in input file")
        print(f"Columns: {list(rows[0].keys()) if rows else 'none'}")
        return rows
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None
