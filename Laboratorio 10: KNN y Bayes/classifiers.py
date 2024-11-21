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

class KNNClassifier:
    def __init__(self):
        self.n_neighbors = 1
        
    def fit(self, X, y):
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        distances = np.linalg.norm(X[:, np.newaxis] - self.X_train, axis=2)
        nearest_indices = np.argsort(distances, axis=1)[:, :self.n_neighbors]
        nearest_labels = self.y_train[nearest_indices]
        return np.array([np.argmax(np.bincount(labels)) for labels in nearest_labels])

class NaiveBayesClassifier:
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        self.priors_ = {}
        self.means_ = {}
        self.vars_ = {}
        epsilon = 1e-9  # Evitar división por cero

        for cls in self.classes_:
            X_c = X[y == cls]
            self.priors_[cls] = X_c.shape[0] / X.shape[0]
            self.means_[cls] = X_c.mean(axis=0)
            self.vars_[cls] = X_c.var(axis=0) + epsilon

    def predict(self, X):
        log_probs = np.zeros((X.shape[0], len(self.classes_)))

        for idx, cls in enumerate(self.classes_):
            prior = np.log(self.priors_[cls])
            # Calcular el logaritmo de la función de densidad de probabilidad gaussiana
            log_likelihood = -0.5 * np.sum(np.log(2. * np.pi * self.vars_[cls]))
            log_likelihood -= 0.5 * np.sum(((X - self.means_[cls]) ** 2) / self.vars_[cls], axis=1)
            log_probs[:, idx] = prior + log_likelihood

        return self.classes_[np.argmax(log_probs, axis=1)]