def parse_salary(raw):
    """Parse a salary string into an integer number of dollars.

    Handles plain integers ('95000') and currency-formatted strings ('$72,500').
    Returns 0 if the value cannot be parsed.
    """
    try:
        return int(raw.strip())
    except ValueError:
        # Attempt to handle comma-separated values
        cleaned = raw.strip().replace(',', '')
        try:
            return int(cleaned)
        except ValueError:
            return 0
