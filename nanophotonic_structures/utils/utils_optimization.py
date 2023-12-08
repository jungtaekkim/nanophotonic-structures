import numpy as np

from nanophotonic_structures.surrogates import train_test
from nanophotonic_structures.utils import utils_properties


def evaluate_discrete(bx, str_structure, X, by):
    assert isinstance(str_structure, str)
    assert len(bx.shape) == 1
    assert len(X.shape) == 2
    assert len(by.shape) == 1
    assert X.shape[0] == by.shape[0]
    assert bx.shape[1] == X.shape[1]

    X, by = utils_properties.filter_values(X, by)

    dist = np.linalg.norm(X - bx, ord=2, axis=1)
    ind = np.argmin(dist)

    evaluation = by[ind]

    if str_structure in ['nanocones2d', 'nanocones3d']:
        return 1.0 * evaluation
    else:
        return -1.0 * evaluation

def evaluate_continuous(bx, str_structure, model):
    assert isinstance(str_structure, str)
    assert len(bx.shape) == 1

    evaluation = train_test.predict(model, bx)

    if str_structure in ['nanocones2d', 'nanocones3d']:
        return 1.0 * evaluation
    else:
        return -1.0 * evaluation
