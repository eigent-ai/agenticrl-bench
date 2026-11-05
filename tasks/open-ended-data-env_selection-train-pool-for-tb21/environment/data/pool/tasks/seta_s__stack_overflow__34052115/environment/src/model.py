"""Model training module using BaggingClassifier with LogisticRegression."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import BaggingClassifier


def train_model(X_train, y_train):
    """Train a BaggingClassifier with LogisticRegression base estimator."""
    base_model = LogisticRegression(random_state=42, max_iter=1000, C=1.0)
    model = BaggingClassifier(
        estimator=base_model,
        n_estimators=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    return model


def get_coefficients(model):
    """Extract coefficients from the trained model."""
    return model.coef_
