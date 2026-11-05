"""JSON serialization for variable inspection reports.

Handles conversion of captured variable data into JSON format
suitable for diagnostic reporting.
"""

import json
import os


def serialize_report(data, output_path):
    """Serialize the captured variable data to a JSON report file.

    Args:
        data: Dictionary containing all captured variable data and metadata.
        output_path: Path to write the JSON report to.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)


def format_value(value):
    """Format a single value for inclusion in the report.

    Args:
        value: Any Python object.

    Returns:
        The value if JSON-serializable, otherwise a string representation.
    """
    try:
        json.dumps(value)
        return value
    except (TypeError, ValueError):
        return str(value)
