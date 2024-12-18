from ucimlrepo import fetch_ucirepo
from classifiers import EuclideanClassifier, Classifier1NN
from validation import hold_out, k_fold_cv, leave_one_out
import numpy as np

# Function to load and proccess dataset
def load_and_process_dataset(id):
    dataset = fetch_ucirepo(id=id)
    X = dataset.data.features.to_numpy()
    y_strings = dataset.data.targets.to_numpy().ravel()
    classes, y = np.unique(y_strings, return_inverse=True)
    return X, y, dataset.metadata

# Load datasets
dataset_ids = [53, 109, 936]

# Classifiers
euclidean_clf = EuclideanClassifier()
knn_clf = Classifier1NN()

# File to save results
results_file = "Laboratorio 9: Clasificadores Euclidiano y 1NN/results.txt"

with open(results_file, "w") as file:
    for dataset_id in dataset_ids:
        X, y, metadata = load_and_process_dataset(id=dataset_id)
        dataset_name = metadata['name']
        dataset_abstract = metadata['abstract']
        
        # Save dataset information
        file.write(f"\n\nDataset Name: {dataset_name}\n")
        file.write(f"Abstract: {dataset_abstract}\n\n")
        
        # Hold Out
        accuracy, cm = hold_out(euclidean_clf, X, y)
        file.write(f"EuclideanClassifier Hold Out Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        accuracy, cm = hold_out(knn_clf, X, y)
        file.write(f"1NNClassifier Hold Out Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        # 10-Fold Cross Validation
        accuracy, cm = k_fold_cv(euclidean_clf, X, y)
        file.write(f"EuclideanClassifier 10-Fold CV Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        accuracy, cm = k_fold_cv(knn_clf, X, y)
        file.write(f"1NNClassifier 10-Fold CV Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        # Leave One Out
        accuracy, cm = leave_one_out(euclidean_clf, X, y)
        file.write(f"EuclideanClassifier Leave One Out Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

        accuracy, cm = leave_one_out(knn_clf, X, y)
        file.write(f"1NNClassifier Leave One Out Accuracy: {accuracy}\n")
        file.write(f"Confusion Matrix:\n{cm}\n\n")

print("Task completed!")