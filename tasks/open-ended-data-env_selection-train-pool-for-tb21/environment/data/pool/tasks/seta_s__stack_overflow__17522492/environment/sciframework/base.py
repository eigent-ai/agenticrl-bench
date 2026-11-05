"""Base classes for the scientific data processing framework."""

from dataclasses import dataclass, field
from typing import Any, Dict


class Data:
    """Base class for data loaders."""

    def load(self, filepath):
        raise NotImplementedError

    def save(self, filepath, data):
        raise NotImplementedError


class Analysis:
    """Base class for analysis operations."""

    def process(self, data):
        """Process the data through analysis pipeline.

        Uses template method pattern: subclasses implement _compute().
        """
        validated = self._validate(data)
        result = self._compute(validated)
        return result

    def _validate(self, data):
        if not data:
            raise ValueError("Empty data provided")
        return data

    def _compute(self, data):
        raise NotImplementedError("Subclasses must implement computation")


class Visualization:
    """Base class for visualization/reporting."""

    def visualize(self, result, output_path):
        raise NotImplementedError


@dataclass
class Result:
    """Container for analysis results."""
    data: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    source_name: str = ""
