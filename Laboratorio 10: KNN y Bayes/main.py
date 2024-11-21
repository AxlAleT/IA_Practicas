from ucimlrepo import fetch_ucirepo
from classifiers import EuclideanClassifier, Classifier1NN, KNNClassifier, NaiveBayesClassifier
from validation import hold_out, k_fold_cv, leave_one_out
import numpy as np

# Function to load and process dataset
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
knn1_clf = Classifier1NN()
knn_clf = KNNClassifier()
nb_clf = NaiveBayesClassifier()

classifiers = {
    "EuclideanClassifier": euclidean_clf,
    "1NNClassifier": knn1_clf,
    "KNNClassifier": knn_clf,
    "NaiveBayesClassifier": nb_clf
}

# File to save results
results_file = "Laboratorio 10/results.txt"

with open(results_file, "w") as file:
    for dataset_id in dataset_ids:
        X, y, metadata = load_and_process_dataset(id=dataset_id)
        dataset_name = metadata['name']
        dataset_abstract = metadata['abstract']
        
        # Save dataset information
        file.write(f"\n\nDataset Name: {dataset_name}\n")
        file.write(f"Abstract: {dataset_abstract}\n\n")
        
        for clf_name, clf in classifiers.items():
            # Hold Out
            accuracy, cm = hold_out(clf, X, y)
            file.write(f"{clf_name} Hold Out Accuracy: {accuracy}\n")
            file.write(f"Confusion Matrix:\n{cm}\n\n")
            
            # 10-Fold Cross Validation
            accuracy, cm = k_fold_cv(clf, X, y)
            file.write(f"{clf_name} 10-Fold CV Accuracy: {accuracy}\n")
            file.write(f"Confusion Matrix:\n{cm}\n\n")
            
            # Leave One Out
            accuracy, cm = leave_one_out(clf, X, y)
            file.write(f"{clf_name} Leave One Out Accuracy: {accuracy}\n")
            file.write(f"Confusion Matrix:\n{cm}\n\n")

print("Task completed!")