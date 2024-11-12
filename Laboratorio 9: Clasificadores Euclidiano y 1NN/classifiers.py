import numpy as np

class EuclideanClassifier:
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        self.centroids_ = np.array([X[y == c].mean(axis=0) for c in self.classes_])

    def predict(self, X):
        distances = np.linalg.norm(X[:, np.newaxis] - self.centroids_, axis=2)
        return self.classes_[np.argmin(distances, axis=1)]

class Classifier1NN:
    def __init__(self):
        self.n_neighbors = 1
        
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        distances = np.linalg.norm(X[:, np.newaxis] - self.X_train, axis=2)
        nearest_indices = np.argsort(distances, axis=1)[:, :self.n_neighbors]
        nearest_labels = self.y_train[nearest_indices]
        nearest_label = nearest_labels[:, 0]
        return nearest_label