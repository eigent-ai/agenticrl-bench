"""Module D — Math utility functions."""

def clamp(value, low, high):
    return max(low, min(high, value))

def average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)
