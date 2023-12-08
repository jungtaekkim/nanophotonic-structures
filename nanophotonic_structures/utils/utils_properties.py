import numpy as np


def filter_values(X, by):
    indices = np.logical_and(by >= 0, by <= 1)

    X = X[indices]
    by = by[indices]

    return X, by
