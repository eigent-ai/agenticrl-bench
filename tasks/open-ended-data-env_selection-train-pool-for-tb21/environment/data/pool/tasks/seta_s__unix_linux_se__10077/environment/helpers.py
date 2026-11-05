"""Helper utilities for data pipeline processing."""


def clean_data(rows):
    """Clean and validate data rows.

    Removes rows with missing or invalid values and strips whitespace
    from category names.
    """
    cleaned = []
    for row in rows:
        category = row.get("category", "").strip()
        value = row.get("value", "").strip()
        if not category or not value:
            continue
        try:
            int(value)
        except ValueError:
            continue
        row["category"] = category
        row["value"] = value
        cleaned.append(row)
    return cleaned
