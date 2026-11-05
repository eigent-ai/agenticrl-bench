from sklearn.svm import SVC
import numpy as np

class SVMModel:
    def __init__(self):
        self.clf = SVC(kernel='rbf', random_state=42)

    def fit(self, X, y):
        self.clf.fit(X, y)
        return self

    def predict(self, X):
        return self.clf.predict(X)

    def score(self, X, y):
        return self.clf.score(X, y)

    def get_support_vectors(self):
        return self.clf.support_vectors_

    def get_model_info(self):
        return {
            "kernel": "linear",
            "n_support": self.clf.n_support_.tolist(),
        }
