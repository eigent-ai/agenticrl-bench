"""Feature importance computation module."""
import numpy as np


def compute_importance(coefficients, X_train, feature_names):
    """Compute feature importance from model coefficients."""
    importance = coefficients.flatten()
    return importance


def map_feature_names(feature_names, categorical_features):
    """Map transformed feature names back to original feature names."""
    mapped = {}
    for name in feature_names:
        if '__' in name:
            stripped = name.split('__', 1)[1]
        else:
            stripped = name
        original = stripped.split('_')[0]
        if original not in mapped:
            mapped[original] = []
        mapped[original].append(name)
    return mapped


def aggregate_importance(importance, feature_names, categorical_features):
    """Aggregate importance scores, combining one-hot encoded features."""
    name_mapping = map_feature_names(feature_names, categorical_features)

    aggregated = {}
    for original_name, child_names in name_mapping.items():
        indices = [list(feature_names).index(n) for n in child_names]
        child_importance = importance[indices]
        aggregated[original_name] = float(np.max(child_importance))

    return aggregated
