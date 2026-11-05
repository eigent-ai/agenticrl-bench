"""Utility functions for classification metrics computation."""

import numpy as np
from sklearn.metrics import confusion_matrix, f1_score, precision_recall_fscore_support


def compute_weighted_f1(y_true, y_pred):
    """Compute weighted F1 score manually using per-class F1 and support.

    Returns a single scalar: the support-weighted average of per-class F1 scores.
    """
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average=None, zero_division=0
    )

    weighted_f1 = np.sum(f1 * support) / len(support)
    return float(weighted_f1)


def compute_confusion_matrices(y_true, y_pred):
    """Compute confusion matrix for classification results.

    Returns the confusion matrix as a nested list suitable for JSON serialization.
    """
    cm = confusion_matrix(y_true, y_pred)
    return cm.tolist()
