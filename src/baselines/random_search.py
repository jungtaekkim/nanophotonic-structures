import numpy as np


def random_search(bx, bounds, fun_target, num_iter, seed):
    X_ = np.random.RandomState(seed * 42 + 1001).uniform(size=(num_iter - 1, bounds.shape[0]))
    X_ = (bounds[:, 1] - bounds[:, 0]) * X_ + bounds[:, 0]

    X = np.concatenate([[bx], X_], axis=0)
    Y = []

    for bx in X:
        Y.append([fun_target(bx)])

    Y = np.array(Y)

    assert X.shape[0] == num_iter
    assert Y.shape[0] == num_iter
    return X, Y
