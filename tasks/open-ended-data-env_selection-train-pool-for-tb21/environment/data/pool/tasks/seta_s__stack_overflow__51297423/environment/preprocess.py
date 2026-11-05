import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class Preprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=3)

    def fit_transform(self, X):
        X_pca = self.pca.fit_transform(X)
        X_scaled = self.scaler.fit_transform(X_pca)
        return X_scaled

    def transform(self, X):
        X_pca = self.pca.transform(X)
        X_scaled = self.scaler.transform(X_pca)
        return X_scaled

    def get_explained_variance(self):
        return self.pca.explained_variance_ratio_.tolist()
