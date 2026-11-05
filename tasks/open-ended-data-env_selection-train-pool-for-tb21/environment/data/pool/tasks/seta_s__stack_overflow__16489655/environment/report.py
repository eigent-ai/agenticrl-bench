import json
import os


def save_report(data, filepath):
    """Save analysis report as a JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Report saved to {filepath}")
