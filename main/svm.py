from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
import sys
import file_manager as fl

def test_svm(x_train, y_train, x_test, y_test):
    tuned_parameters = [
        {'kernel': ['rbf'], 'gamma': [1e-3, 1e-4], 'C': [1, 10, 100, 1000]},
        {'kernel': ['linear'], 'C': [1, 10, 100, 1000], 'max_iter': [5000]},
        {'kernel': ['poly'], 'C': [1, 10, 100, 1000], 'degree': [3, 4, 5], 'gamma': [1e-3, 1e-4]}
    ]

    clf = GridSearchCV(SVC(probability=True), tuned_parameters, cv=5, n_jobs=-1)
    clf.fit(x_train, y_train)
    print(clf.best_params_)
    svclassifier = clf.best_estimator_
    y_pred = svclassifier.predict(x_test)
    print("Accuracy: {}".format(svclassifier.score(x_test, y_test)))

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))

def test_knn(x_train, y_train, x_test, y_test):
    parameters =[
        {'algorithm': ['auto'], 'leaf_size': [40,30,20], 'metric': ['minkowski', 'chebyshev', 'manhattan']},
    ]

    clf = GridSearchCV(KNeighborsClassifier(), parameters, cv=5, n_jobs=-1)

    clf.fit(x_train, y_train)

    knn = clf.best_estimator_

    y_pred = knn.predict(x_test)

    print("Accuracy: {}".format(knn.score(x_test, y_test)))

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))


if __name__ == '__main__':

    training_file_name = sys.argv[1]
    test_file_name  = sys.argv[2]
    loader = fl.Loader()
    x_train = []
    x_test = []
    extended_x_train, y_train = loader.compute_batch(loader.load_file(training_file_name))
    for gesture in extended_x_train:
        frames = []
        for frame in gesture:
                for elem in frame:
                    frames.append(elem)
        x_train.append(frames)

    extended_x_test, y_test = loader.compute_batch(loader.load_file(test_file_name))

    for gesture in extended_x_test:
        frames = []
        for frame in gesture:
                for elem in frame:
                    frames.append(elem)
        x_test.append(frames)

    #test_svm(x_train, y_train, x_test, y_test)

    test_knn(x_train, y_train, x_test, y_test)
