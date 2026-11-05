from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


def compute_metrics(y_true, y_pred_default, y_pred_thresholded):
    """Compute classification metrics for model evaluation.

    Parameters
    ----------
    y_true : array-like
        Ground truth labels.
    y_pred_default : array-like
        Predictions using default decision boundary.
    y_pred_thresholded : array-like
        Predictions using custom threshold from config.

    Returns
    -------
    dict
        Dictionary containing precision, recall, f1, and accuracy.
    """
    metrics = {
        "precision": float(precision_score(y_true, y_pred_default, zero_division=0)),
        "recall": float(recall_score(y_true, y_pred_default, zero_division=0)),
        "f1": float(f1_score(y_true, y_pred_default, zero_division=0)),
        "accuracy": float(accuracy_score(y_true, y_pred_default)),
    }
    return metrics
