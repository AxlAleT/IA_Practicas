import tensorflow as tf
import numpy as np
import os
import pickle

class RBFClassifier:
    def __init__(self, num_centers=10, sigma=1.0, epochs=100, batch_size=32):
        self.num_centers = num_centers
        self.sigma = sigma
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None
        self.centers = None  # Store centers

    def fit(self, X, y, dataset_id, validation_method):
        if validation_method == 'hold_out':
            model_path = f"Laboratorio 11: Redes Neuronales/rbf_model_{dataset_id}_{validation_method}.h5"
            centers_path = f"Laboratorio 11: Redes Neuronales/rbf_centers_{dataset_id}_{validation_method}.pkl"
            if os.path.exists(model_path) and os.path.exists(centers_path):
                self.model = tf.keras.models.load_model(model_path)
                with open(centers_path, 'rb') as f:
                    self.centers = pickle.load(f)
                return
        # Select random centers from X
        indices = np.random.choice(len(X), self.num_centers, replace=False)
        self.centers = X[indices]
        # Compute RBF features
        diff = X[:, np.newaxis, :] - self.centers[np.newaxis, :, :]
        rbf_features = np.exp(-np.sum(diff ** 2, axis=2) / (2 * self.sigma ** 2))
        # Build and train model
        self.model = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(self.num_centers,)),
            tf.keras.layers.Dense(len(np.unique(y)), activation='softmax')
        ])
        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])
        self.model.fit(rbf_features, y, epochs=self.epochs, batch_size=self.batch_size, verbose=0)
        if validation_method == 'hold_out':
            self.model.save(model_path)
            with open(centers_path, 'wb') as f:
                pickle.dump(self.centers, f)

    def predict(self, X, dataset_id, validation_method):
        if self.model is None and validation_method == 'hold_out':
            model_path = f"Laboratorio 11: Redes Neuronales/rbf_model_{dataset_id}_{validation_method}.h5"
            centers_path = f"Laboratorio 11: Redes Neuronales/rbf_centers_{dataset_id}_{validation_method}.pkl"
            self.model = tf.keras.models.load_model(model_path)
            with open(centers_path, 'rb') as f:
                self.centers = pickle.load(f)
        # Use the centers determined during training
        diff = X[:, np.newaxis, :] - self.centers[np.newaxis, :, :]
        rbf_features = np.exp(-np.sum(diff ** 2, axis=2) / (2 * self.sigma ** 2))
        predictions = self.model.predict(rbf_features)
        return np.argmax(predictions, axis=1)

class MLPClassifier:
    def __init__(self, hidden_layer_sizes=(100,), activation='relu', epochs=100, batch_size=32):
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation = activation
        self.epochs = epochs
        self.batch_size = batch_size
        self.model = None

    def fit(self, X, y, dataset_id, validation_method):
        if validation_method == 'hold_out':
            model_path = f"Laboratorio 11: Redes Neuronales/mlp_model_{dataset_id}_{validation_method}.h5"
            if os.path.exists(model_path):
                self.model = tf.keras.models.load_model(model_path)
                return
        self.model = tf.keras.Sequential()
        self.model.add(tf.keras.layers.InputLayer(input_shape=(X.shape[1],)))
        for units in self.hidden_layer_sizes:
            self.model.add(tf.keras.layers.Dense(units, activation=self.activation))
        self.model.add(tf.keras.layers.Dense(len(np.unique(y)), activation='softmax'))
        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])
        self.model.fit(X, y, epochs=self.epochs, batch_size=self.batch_size, verbose=0)
        if validation_method == 'hold_out':
            self.model.save(model_path)

    def predict(self, X, dataset_id, validation_method):
        if self.model is None and validation_method == 'hold_out':
            model_path = f"Laboratorio 11: Redes Neuronales/mlp_model_{dataset_id}_{validation_method}.h5"
            if os.path.exists(model_path):
                self.model = tf.keras.models.load_model(model_path)
        predictions = self.model.predict(X)
        return np.argmax(predictions, axis=1)