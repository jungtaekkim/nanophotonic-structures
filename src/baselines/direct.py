import numpy as np
import scipy.optimize as sciop

from baselines.objective import Objective


def direct(bx, bounds, fun_target, num_iter):
    obj_target = Objective(fun_target, bounds)

    if num_iter > 0:
        result = sciop.direct(
            obj_target,
            list(obj_target.bounds_filtered),
            maxiter=num_iter,
            maxfun=num_iter
        )

    X = np.array(np.concatenate([[bx], obj_target.X], axis=0))
    Y = np.array(np.concatenate([[[fun_target(bx)]], obj_target.Y], axis=0))

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
