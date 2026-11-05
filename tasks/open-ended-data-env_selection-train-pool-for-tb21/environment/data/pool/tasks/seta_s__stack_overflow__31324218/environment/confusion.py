import numpy as np


def extract_per_class_metrics(cm):
    """Extract per-class TP, FP, TN, FN from a confusion matrix using one-vs-rest."""
    num_classes = cm.shape[0]
    total = cm.sum()
    results = []
    for i in range(num_classes):
        tp = cm[i, i]
        fp = cm[i, :].sum() - tp
        fn = cm[:, i].sum() - tp
        tn = total - tp - fp - fn
        results.append({
            "class": i,
            "TP": int(tp),
            "FP": int(fp),
            "TN": int(tn),
            "FN": int(fn),
        })
    return results
