import csv


def load_items(filepath):
    """Load item records from a CSV file.

    Expected columns: id, name, category, weight
    Returns a list of dicts.
    """
    items = []
    with open(filepath, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            items.append({
                'id': int(row['id']),
                'name': row['name'].strip(),
                'category': row['category'].strip(),
                'weight': float(row['weight']),
            })
    return items
