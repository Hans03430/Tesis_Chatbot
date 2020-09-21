import numpy as np
import pandas as pd

from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from typing import Iterable
from typing import List


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
    
    
def print_scores(y_true: Iterable, y_pred: Iterable) -> None:
	'''
	This function prints the accuracy, precision, recall and f1 score of a prediction.
	
	Parameters:
	y_true(Iterable): Iterable containing the true labels.
	y_pred(Iterable): Iterable containing the predicted labels.
	
	Returns:
	None.
	'''
	print(f'The accuracy score is: {accuracy_score(y_true, y_pred)}')
	print(f'The precision score is: {precision_score(y_true, y_pred)}')
	print(f'The recall score is: {recall_score(y_true, y_pred)}')
	print(f'The F1 score is: {f1_score(y_true, y_pred)}')
