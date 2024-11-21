import numpy as np

def hold_out(classifier, X, y, test_size=0.3):
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    split = int(len(X) * (1 - test_size))
    train_indices = indices[:split]
    test_indices = indices[split:]

    X_train, y_train = X[train_indices], y[train_indices]
    X_test, y_test = X[test_indices], y[test_indices]

    classifier.fit(X_train, y_train)
    y_pred = classifier.predict(X_test)

    accuracy = np.mean(y_pred == y_test)
    cm = confusion_matrix(y_test, y_pred)
    return accuracy, cm

def k_fold_cv(classifier, X, y, n_splits=10):
    indices = np.arange(len(X))
    np.random.shuffle(indices)
    folds = np.array_split(indices, n_splits)
    accuracies = []
    cms = []
    for i in range(n_splits):
        test_indices = folds[i]
        train_indices = np.concatenate(folds[:i] + folds[i+1:])
        X_train, y_train = X[train_indices], y[train_indices]
        X_test, y_test = X[test_indices], y[test_indices]

        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        accuracies.append(np.mean(y_pred == y_test))
        cms.append(confusion_matrix(y_test, y_pred))
    return np.mean(accuracies), sum(cms)

def leave_one_out(classifier, X, y):
    accuracies = []
    cms = []
    for i in range(len(X)):
        X_train = np.delete(X, i, axis=0)
        y_train = np.delete(y, i)
        X_test = X[i].reshape(1, -1)
        y_test = y[i]

        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)
        accuracies.append(y_pred[0] == y_test)
        cms.append(confusion_matrix([y_test], y_pred))
    return np.mean(accuracies), sum(cms)

def confusion_matrix(y_true, y_pred):
    classes = np.unique(np.concatenate((y_true, y_pred)))
    cm = np.zeros((len(classes), len(classes)), dtype=int)
    class_to_index = {label: index for index, label in enumerate(classes)}
    for true, pred in zip(y_true, y_pred):
        cm[class_to_index[true], class_to_index[pred]] += 1
    return cm