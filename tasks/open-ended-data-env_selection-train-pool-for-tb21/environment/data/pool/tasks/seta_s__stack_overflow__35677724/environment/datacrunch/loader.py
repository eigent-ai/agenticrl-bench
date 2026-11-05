import csv


class DataLoader:
    """Loads data from CSV files as streams of float values."""

    def __init__(self):
        self._cache = {}

    def load(self, filepath):
        """Load a CSV file and yield each value as a float.

        Args:
            filepath: Path to a CSV file with a single column of numeric values.

        Yields:
            float: Each value from the CSV file.
        """
        with open(filepath, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            for row in reader:
                yield float(row[0])
