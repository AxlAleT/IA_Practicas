from ucimlrepo import fetch_ucirepo
from classifiers import RBFClassifier, MLPClassifier
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
dataset_ids = [42]#, 109, 936]

results_file = "Laboratorio 11: Redes Neuronales/results.txt"

with open(results_file, "w") as file:
    for dataset_id in dataset_ids:
        X, y, metadata = load_and_process_dataset(id=dataset_id)
        classes = np.unique(y)
        dataset_name = metadata['name']
        dataset_abstract = metadata['abstract']
        
        # Save dataset information
        file.write(f"\n\nDataset Name: {dataset_name}\n")
        file.write(f"Abstract: {dataset_abstract}\n\n")

        # Initialize classifiers for each dataset
        mlp_clf = MLPClassifier(hidden_layer_sizes=(20, 10), activation='relu', epochs=100, batch_size=16)
        rbf_clf = RBFClassifier(num_centers=30, sigma=0.5, epochs=100, batch_size=16)

        classifiers = {
            "MLPClassifier": mlp_clf,
            "RBFClassifier": rbf_clf,
        }
        
        for clf_name, clf in classifiers.items():
            # Hold Out
            accuracy, cm = hold_out(clf, X, y, labels=classes, dataset_id=dataset_id)
            file.write(f"{clf_name} Hold Out Accuracy: {accuracy}\n")
            file.write(f"Confusion Matrix:\n{cm}\n\n")
            
            # 10-Fold Cross Validation
            accuracy, cm = k_fold_cv(clf, X, y, labels=classes, dataset_id=dataset_id)
            file.write(f"{clf_name} 10-Fold CV Accuracy: {accuracy}\n")
            file.write(f"Confusion Matrix:\n{cm}\n\n")
            
            # Leave One Out
            accuracy, cm = leave_one_out(clf, X, y, labels=classes, dataset_id=dataset_id)
            file.write(f"{clf_name} Leave One Out Accuracy: {accuracy}\n")
            file.write(f"Confusion Matrix:\n{cm}\n\n")

print("Task completed!")