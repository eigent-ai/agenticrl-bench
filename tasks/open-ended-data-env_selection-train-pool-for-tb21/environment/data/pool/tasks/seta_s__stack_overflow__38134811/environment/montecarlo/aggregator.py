import numpy as np


class ResultAggregator:
    """Aggregates batch results from multiple simulation runs."""

    def __init__(self):
        self.results = []

    def collect_results(self, batch_results):
        """Aggregate a list of batch result arrays into a single flat array.

        Parameters
        ----------
        batch_results : list of array-like
            Each element is a batch of samples.

        Returns
        -------
        np.ndarray
            Combined 1-D array of all samples.
        """
        all_samples = []
        for batch_result in batch_results:
            all_samples.append(batch_result)
        return np.array(all_samples)
