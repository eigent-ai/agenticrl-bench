import json
from datetime import datetime


def write_report(results, output_path):
    """Write pipeline results to a JSON report file.

    Args:
        results: Dictionary of computed statistics.
        output_path: Path to write the JSON report.
    """
    report = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%m:%S"),
        "results": results,
    }

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return report
