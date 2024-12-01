import numpy as np
import tensorflow as tf

# Enable GPU growth to utilize GPU resources efficiently
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)

def hold_out(classifier, X, y, test_size=0.3, labels=None, dataset_id=None):
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    split = int(len(X) * (1 - test_size))
    train_indices = indices[:split]
    test_indices = indices[split:]

    X_train, y_train = X[train_indices], y[train_indices]
    X_test, y_test = X[test_indices], y[test_indices]

    validation_method = 'hold_out'
    classifier.fit(X_train, y_train, dataset_id, validation_method)
    y_pred = classifier.predict(X_test, dataset_id, validation_method)

    accuracy = np.mean(y_pred == y_test)
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    return accuracy, cm

def k_fold_cv(classifier, X, y, n_splits=10, labels=None, dataset_id=None):
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    folds = np.array_split(indices, n_splits)
    accuracies = []
    cms = []
    validation_method = 'k_fold'
    for i in range(n_splits):
        test_indices = folds[i]
        train_indices = np.concatenate(folds[:i] + folds[i+1:])
        X_train, y_train = X[train_indices], y[train_indices]
        X_test, y_test = X[test_indices], y[test_indices]

        classifier.fit(X_train, y_train, dataset_id, validation_method)
        y_pred = classifier.predict(X_test, dataset_id, validation_method)
        accuracies.append(np.mean(y_pred == y_test))
        cms.append(confusion_matrix(y_test, y_pred, labels=labels))
    total_cm = np.sum(cms, axis=0)
    return np.mean(accuracies), total_cm

def leave_one_out(classifier, X, y, labels=None, dataset_id=None):
    accuracies = []
    cms = []
    validation_method = 'leave_one_out'
    for i in range(len(X)):
        X_train = np.delete(X, i, axis=0)
        y_train = np.delete(y, i)
        X_test = X[i].reshape(1, -1)
        y_test = y[i]

        classifier.fit(X_train, y_train, dataset_id, validation_method)
        y_pred = classifier.predict(X_test, dataset_id, validation_method)
        accuracies.append(y_pred[0] == y_test)
        cms.append(confusion_matrix([y_test], y_pred, labels=labels))
    total_cm = np.sum(cms, axis=0)
    return np.mean(accuracies), total_cm

def confusion_matrix(y_true, y_pred, labels):
    cm = np.zeros((len(labels), len(labels)), dtype=int)
    class_to_index = {label: index for index, label in enumerate(labels)}
    for true, pred in zip(y_true, y_pred):
        cm[class_to_index[true], class_to_index[pred]] += 1
    return cm