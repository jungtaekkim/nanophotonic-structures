import numpy as np
import pybobyqa as pybbq

from baselines.objective import Objective


def pybobyqa(bx, bounds, fun_target, num_iter):
    obj_target = Objective(fun_target, bounds)

    solutions = pybbq.solve(
        obj_target,
        obj_target.filter(bx),
        bounds=obj_target.bounds_filtered_tuple,
        maxfun=num_iter,
        scaling_within_bounds=True
    )

    X = np.array(obj_target.X)
    Y = np.array(obj_target.Y)

    assert X.shape[0] == Y.shape[0]
    if X.shape[0] < num_iter:
        X = np.concatenate([X, [X[-1]] * (num_iter - X.shape[0])], axis=0)
        Y = np.concatenate([Y, [Y[-1]] * (num_iter - Y.shape[0])], axis=0)
    if X.shape[0] > num_iter:
        X = X[:num_iter]
        Y = Y[:num_iter]

    assert X.shape[0] == num_iter
    assert Y.shape[0] == num_iter
    return X, Y
