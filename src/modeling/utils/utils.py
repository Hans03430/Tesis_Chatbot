import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from typing import Iterable
from typing import List
from typing import Dict


def drop_dataset_unnecessary_columns(dataset: pd.DataFrame, cols_to_drop: List[str], target_col: str) -> (pd.DataFrame, pd.DataFrame):
    '''
    This function drops the columns from the dataset and returns X and y.

    Parameters:
    dataset(pd.DataFrame): The dataframe whose columns to drop.
    cols_to_drop(List[str]): The name of the columns to drop.
    target_col(str): The name of the target column.

    Returns:
    (pd.DataFrame, pd.DataFrame): X and y datasets.
    '''
    no_null = dataset.dropna()
    X = no_null.drop(columns=cols_to_drop).copy()
    y = no_null[target_col].copy()
    return X, y


def pca(dataset: pd.DataFrame, n_components: int=2) -> np.array:
    '''
    This function does the principal component analysis.

    Parameters:
    dataset(pd.DataFrame): The dataset to reduce dimensionality.
    n_components(int): The amount of dimensions to reduce the dataset:

    Returns:
    np.array: Numpy array that contains the pca values.
    '''
    pca = PCA(n_components=n_components)
    pca.fit(dataset)
    X = pca.transform(dataset)
    return X
    
    
def print_scores(y_true: Iterable, y_pred: Iterable) -> Dict:
    '''
    This function prints the accuracy, precision, recall and f1 score of a prediction.

    Parameters:
    y_true(Iterable): Iterable containing the true labels.
    y_pred(Iterable): Iterable containing the predicted labels.

    Returns:
    Dict: The dictionary with the scores.
    '''
    scores = {}
    scores['accuracy'] = accuracy_score(y_true, y_pred)
    scores['precision'] = precision_score(y_true, y_pred)
    scores['recall'] = recall_score(y_true, y_pred)
    scores['f1 score'] = f1_score(y_true, y_pred)

    print(f'The accuracy score is: {scores["accuracy"]}')
    print(f'The precision score is: {scores["precision"]}')
    print(f'The recall score is: {scores["recall"]}')
    print(f'The F1 score is: {scores["f1 score"]}')

    return scores


def train_test_model(model, model_name: str, params: Dict, X_train: Iterable, y_train: Iterable, X_test: Iterable, y_test: Iterable, results: pd.DataFrame, estimators: List=None) -> (pd.DataFrame, Iterable):
    '''
    This function trains a classification model, tests it and save its results in a dataframe.

    Parameters:
    model: A classification model that implements the methods 'fit' and 'predict'.
    model_name(str): The name of the model.
    params(Dict): A dictionary with the model's parameters to pass at creation.
    X_train(Iterable): Attributes to train the model with.
    y_train(Iterable): Targets to train the model with.
    X_test(Iterable): Attributes to test the model with.
    y_test(Iterable): Targets to test the model with.
    results(pd.DataFrame): The pandas dataframe to store the results in.
    estimators(List): List of estimators for voting classifiers

    Returns:
    (pd.DataFrame, Iterable): The dataset with the score results and the predicted labels.
    '''
    if estimators is None:
        clf = model(**params)
    else:
        clf = model(estimators=estimators, **params)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    clf_results = pd.DataFrame(data=print_scores(y_test, y_pred), index=[model_name])
    results = results.append(clf_results)
    return results, y_pred