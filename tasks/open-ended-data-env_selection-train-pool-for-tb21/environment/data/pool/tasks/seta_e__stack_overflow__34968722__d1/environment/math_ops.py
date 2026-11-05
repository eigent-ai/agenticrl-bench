import numpy as np

def softmax(x):
    """Compute softmax probabilities along the last axis."""
    e_x = np.exp(x)
    return e_x / np.sum(e_x, axis=-1, keepdims=True)

def log_softmax(x):
    """Compute log-softmax along the last axis."""
    return np.log(softmax(x))

def cross_entropy(probs, labels):
    """Compute mean cross-entropy loss given probabilities and integer labels."""
    n = probs.shape[0]
    log_probs = np.log(probs[np.arange(n), labels])
    return -np.mean(log_probs)
