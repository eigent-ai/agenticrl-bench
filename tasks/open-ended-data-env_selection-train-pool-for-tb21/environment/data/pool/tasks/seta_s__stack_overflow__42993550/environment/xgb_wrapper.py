import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor


class XGBoostWithEarlyStop(BaseEstimator, RegressorMixin):
    """Wrapper around XGBoost that handles early stopping internally."""

    def __init__(self, early_stopping_rounds=10, test_size=0.2, eval_metric='mae'):
        self.early_stopping_rounds = early_stopping_rounds
        self.test_size = test_size
        self.eval_metric = eval_metric = 'mae'
        self._configure_early_stopping()

    def _configure_early_stopping(self):
        """Apply early stopping settings to the underlying estimator."""
        self.estimator.set_params(
            early_stopping_rounds=self.early_stopping_rounds,
        )

    def fit(self, X, y, **kwargs):
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=self.test_size, random_state=0
        )

        self.estimator.set_params(
            early_stopping_rounds=self.early_stopping_rounds,
            eval_metric=self.eval_metric,
        )

        self.estimator.fit(
            X_train, y_train,
            eval_set=[(X_val, y_val)],
            verbose=False,
        )
        return self

    def predict(self, X):
        return self.estimator.predict(X)

    def get_params(self, **params):
        return self.estimator.get_params()

    def set_params(self, **params):
        wrapper_keys = {'early_stopping_rounds', 'test_size', 'eval_metric'}
        for key, value in params.items():
            if key in wrapper_keys:
                setattr(self, key, value)
            else:
                self.estimator.set_params(**{key: value})
        return self


class XGBoostRegressorWithEarlyStop(XGBoostWithEarlyStop):
    """XGBRegressor with built-in early stopping for use in sklearn Pipelines."""

    def __init__(self, early_stopping_rounds=10, test_size=0.2, eval_metric='mae',
                 n_estimators=100, max_depth=6, learning_rate=0.3, random_state=None,
                 **kwargs):
        super().__init__(
            early_stopping_rounds=early_stopping_rounds,
            test_size=test_size,
            eval_metric=eval_metric,
        )
        self.estimator = XGBRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=random_state,
            **kwargs,
        )
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.learning_rate = learning_rate
        self.random_state = random_state
