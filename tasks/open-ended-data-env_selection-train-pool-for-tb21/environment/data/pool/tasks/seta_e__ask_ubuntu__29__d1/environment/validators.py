def validate_input(value):
    if not isinstance(value, (int, float)):
        raise TypeError("Value must be numeric")
    return True
