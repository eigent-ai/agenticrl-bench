"""Main processing module for the data pipeline."""

import os
import json
from typing import Dict, List, Any
from helpers import find_files, compute_hash, ensure_directory


class DataProcessor:
    """Processes input files and generates structured output."""

    def __init__(self, input_dir: str, output_dir: str):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.results: List[Dict[str, Any]] = []

    def process_all(self) -> None:
        """Process all eligible files in the input directory."""
        ensure_directory(self.output_dir)
        files = find_files(self.input_dir, extensions=[".txt", ".csv", ".json"])

        for filepath in files:
            result = self.process_file(filepath)
            if result:
                self.results.append(result)

    def process_file(self, filepath: str) -> Dict[str, Any]:
        """Process a single file and return metadata."""
        stat = os.stat(filepath)
        return {
            "path": filepath,
            "size": stat.st_size,
            "hash": compute_hash(filepath),
            "extension": os.path.splitext(filepath)[1],
        }

    def write_report(self, output_path: str) -> None:
        """Write processing report as JSON."""
        report = {
            "total_files": len(self.results),
            "total_size": sum(r["size"] for r in self.results),
            "files": self.results,
        }
        with open(output_path, "w") as f:
            json.dump(report, f, indent=2)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python processor.py <input_dir> <output_dir>")
        sys.exit(1)

    proc = DataProcessor(sys.argv[1], sys.argv[2])
    proc.process_all()
    proc.write_report(os.path.join(sys.argv[2], "report.json"))
    print(f"Processed {len(proc.results)} files")
