"""Data ingestion module for the processing pipeline."""

import json
import os


class DataIngestor:
    """Reads raw data files and returns parsed records."""

    def __init__(self, source_dir):
        self.source_dir = source_dir

    def load_records(self, filename):
        path = os.path.join(self.source_dir, filename)
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def list_sources(self):
        return [f for f in os.listdir(self.source_dir) if f.endswith(".json")]
