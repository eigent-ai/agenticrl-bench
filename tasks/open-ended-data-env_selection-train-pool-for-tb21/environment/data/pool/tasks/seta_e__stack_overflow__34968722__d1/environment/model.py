import numpy as np

class LinearClassifier:
    """Simple linear classifier: logits = features @ weights + bias."""
    def __init__(self, weights_path):
        data = np.load(weights_path)
        self.weights = data["weights"]
        self.bias = data["bias"]
        self.num_classes = self.weights.shape[1]

    def forward(self, features):
        """Compute raw logits for a batch of feature vectors."""
        return features @ self.weights + self.bias
