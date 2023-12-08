import numpy as np


def random_search(bx, bounds, num_choices, fun_target, num_iter, seed):
    X_ = np.random.RandomState(seed * 42 + 1001).choice(num_choices, size=(num_iter - 1, bounds.shape[0]))

    X = np.concatenate([[bx], X_], axis=0)
    Y = []

    for ind_bx, bx in enumerate(X):
        print(f'Iteration {ind_bx+1}', flush=True)
        Y.append([fun_target(bx)])
        print(Y, flush=True)

    Y = np.array(Y)

    assert X.shape[0] == num_iter
    assert Y.shape[0] == num_iter
    return X, Y
