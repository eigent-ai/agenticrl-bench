"""Report writer implementation."""

import json
from sciframework.base import Visualization


class ReportWriter(Visualization):
    """Writes analysis results to JSON report files."""

    def __init__(self, name="report_writer"):
        self.name = name

    def visualize(self, result, output_path):
        """Write result to a JSON report file."""
        report = {
            "source": result.source_name,
            "results": result.values,
            "metadata": result.metadata
        }
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
