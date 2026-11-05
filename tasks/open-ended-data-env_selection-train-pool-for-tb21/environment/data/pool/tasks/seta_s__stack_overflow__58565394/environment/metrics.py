import numpy as np

_EPS = 1e-10


def categorical_crossentropy(y_true_onehot, y_pred):
    """Categorical cross-entropy loss.

    Args:
        y_true_onehot: array of shape (N, K), one-hot encoded ground-truth labels.
        y_pred: array of shape (N, K), predicted probabilities (rows sum to 1).

    Returns:
        Scalar mean loss.
    """
    return float(-np.mean(np.sum(y_true_onehot * np.log(np.clip(y_pred, _EPS, 1.0)), axis=1)))


def sparse_categorical_crossentropy(y_true_int, y_pred):
    """Sparse categorical cross-entropy loss.

    Args:
        y_true_int: array of shape (N,), integer class indices.
        y_pred: array of shape (N, K), predicted probabilities (rows sum to 1).

    Returns:
        Scalar mean loss.
    """
    idx = y_true_int.astype(int)
    correct_probs = y_pred[np.arange(len(idx)), idx]
    return float(-np.mean(np.log(np.clip(correct_probs, _EPS, 1.0))))


def categorical_accuracy(y_true_onehot, y_pred):
    """Categorical accuracy.

    Args:
        y_true_onehot: array of shape (N, K), one-hot encoded ground-truth labels.
        y_pred: array of shape (N, K), predicted probabilities.

    Returns:
        Scalar accuracy in [0, 1].
    """
    return float(np.mean(np.argmax(y_true_onehot, axis=1) == np.argmax(y_pred, axis=1)))


def sparse_categorical_accuracy(y_true_int, y_pred):
    """Sparse categorical accuracy.

    Args:
        y_true_int: array of shape (N,), integer class indices.
        y_pred: array of shape (N, K), predicted probabilities.

    Returns:
        Scalar accuracy in [0, 1].
    """
    return float(np.mean(y_true_int.astype(int) == np.argmax(y_pred, axis=1)))


def binary_crossentropy(y_true, y_pred_prob):
    """Binary cross-entropy loss.

    Args:
        y_true: array of shape (N,), binary labels 0 or 1.
        y_pred_prob: array of shape (N,), sigmoid probabilities for the positive class.

    Returns:
        Scalar mean loss.
    """
    p = np.clip(y_pred_prob, _EPS, 1.0 - _EPS)
    return float(-np.mean(y_true * np.log(p) + (1.0 - y_true) * np.log(1.0 - p)))
