"""Clustering analysis implementation."""

import numpy as np
from sciframework.base import Analysis, Result


class ClusteringAnalysis(Analysis):
    """Simple distance-based clustering on numeric columns."""

    def __init__(self, name="clustering", k=3):
        self.name = name
        self.k = k
        self.centroids = None

    def _run_computation(self, data):
        """Assign each row to nearest of k fixed centroids based on first two numeric columns."""
        if not data:
            return Result(data={}, metadata={"algorithm": "kmeans", "k": self.k}, source_name=self.name)

        numeric_cols = []
        for key, value in data[0].items():
            if isinstance(value, (int, float)):
                numeric_cols.append(key)

        if len(numeric_cols) < 2:
            return Result(data={}, metadata={"error": "need at least 2 numeric columns"}, source_name=self.name)

        col1, col2 = numeric_cols[0], numeric_cols[1]
        points = np.array([[r[col1], r[col2]] for r in data])

        min_vals = points.min(axis=0)
        max_vals = points.max(axis=0)
        np.random.seed(42)
        self.centroids = np.array([
            min_vals + (max_vals - min_vals) * (i + 1) / (self.k + 1)
            for i in range(self.k)
        ])

        labels = []
        for point in points:
            distances = [np.sqrt(np.sum((point - c) ** 2)) for c in self.centroids]
            labels.append(int(np.argmin(distances)))

        cluster_counts = {}
        for label in labels:
            cluster_counts[str(label)] = cluster_counts.get(str(label), 0) + 1

        result_data = {
            "labels": labels,
            "cluster_counts": cluster_counts,
            "centroids": self.centroids.tolist(),
            "columns_used": [col1, col2]
        }

        return Result(
            data=result_data,
            metadata={"algorithm": "distance_based", "k": self.k, "n_records": len(data)},
            source_name=self.name
        )
