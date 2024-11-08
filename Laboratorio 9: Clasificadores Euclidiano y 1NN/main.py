from ucimlrepo import fetch_ucirepo
from classifiers import EuclideanClassifier, KNNClassifier
from validation import hold_out, k_fold_cv, leave_one_out
import numpy as np

# Función para cargar y procesar datasets
def load_and_process_dataset(id):
    dataset = fetch_ucirepo(id=id)
    X = dataset.data.features.to_numpy()
    y_strings = dataset.data.targets.to_numpy().ravel()
    classes, y = np.unique(y_strings, return_inverse=True)
    return X, y, dataset.metadata

# Cargar datasets
dataset_ids = [53, 109, 936]

# Clasificadores
euclidean_clf = EuclideanClassifier()
knn_clf = KNNClassifier(n_neighbors=1)

# Archivo para guardar resultados
results_file = "Laboratorio 9: Clasificadores Euclidiano y 1NN/results.txt"

with open(results_file, "w") as file:
    for dataset_id in dataset_ids:
        X, y, metadata = load_and_process_dataset(id=dataset_id)
        dataset_name = metadata['name']
        dataset_abstract = metadata['abstract']
        
        # Guardar nombre y abstract en el archivo
        file.write(f"\n\nDataset Name: {dataset_name}\n")
        file.write(f"Abstract: {dataset_abstract}\n\n")
        
        # Hold Out
        accuracy, cm = hold_out(euclidean_clf, X, y)
        file.write(f"EuclideanClassifier Hold Out Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        accuracy, cm = hold_out(knn_clf, X, y)
        file.write(f"KNNClassifier Hold Out Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        # 10-Fold Cross Validation
        accuracy, cm = k_fold_cv(euclidean_clf, X, y)
        file.write(f"EuclideanClassifier 10-Fold CV Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        accuracy, cm = k_fold_cv(knn_clf, X, y)
        file.write(f"KNNClassifier 10-Fold CV Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        # Leave One Out
        accuracy, cm = leave_one_out(euclidean_clf, X, y)
        file.write(f"EuclideanClassifier Leave One Out Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        accuracy, cm = leave_one_out(knn_clf, X, y)
        file.write(f"KNNClassifier Leave One Out Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")