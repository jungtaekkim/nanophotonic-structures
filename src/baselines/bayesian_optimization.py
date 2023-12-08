import numpy as np
from bayeso import bo as bayesobo


def bayesian_optimization(bx, bounds, fun_target, num_iter, seed):
    X = [bx]
    Y = [[fun_target(bx)]]

    model_bo = bayesobo.BOwGP(bounds, str_acq='ei', str_cov='matern52')

    for ind_iter in range(0, num_iter - 1):
        print(f'Iteration {ind_iter+1}', flush=True)
        next_point, _ = model_bo.optimize(np.array(X), np.array(Y), seed=seed * 142 + ind_iter + 101)

        X.append(next_point)
        Y.append([fun_target(next_point)])

    X = np.array(X)
    Y = np.array(Y)

    assert X.shape[0] == num_iter
    assert Y.shape[0] == num_iter
    return X, Y
