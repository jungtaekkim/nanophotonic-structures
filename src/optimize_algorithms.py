import numpy as np
import argparse
import os

from nanophotonic_structures import constants
from nanophotonic_structures.surrogates import train_test
from nanophotonic_structures.utils import utils_structures
from nanophotonic_structures.utils import utils_optimization

import baselines.pybobyqa as pybobyqa
import baselines.powell as powell
import baselines.differential_evolution as differential_evolution
import baselines.direct as direct
import baselines.bayesian_optimization as bayesian_optimization
import baselines.random_search as random_search

import constants as constants_src


path_trained_models = constants_src.path_trained_models
path_optimization_results = constants_src.path_optimization_results


def run_algorithm(str_algorithm, bx_initial, bounds, fun_target, num_iter, seed):
    if str_algorithm == 'pybobyqa':
        # seed is not used.

        X, Y = pybobyqa.pybobyqa(bx_initial, bounds, fun_target, num_iter)
    elif str_algorithm == 'powell':
        # seed is not used.

        X, Y = powell.powell(bx_initial, bounds, fun_target, num_iter)
    elif str_algorithm == 'de':
        # seed is not used.

        X, Y = differential_evolution.differential_evolution(bx_initial, bounds, fun_target, num_iter)
    elif str_algorithm == 'direct':
        # seed is not used.

        X, Y = direct.direct(bx_initial, bounds, fun_target, num_iter)
    elif str_algorithm == 'bo':
        X, Y = bayesian_optimization.bayesian_optimization(bx_initial, bounds, fun_target, num_iter, seed)
    elif str_algorithm == 'rs':
        X, Y = random_search.random_search(bx_initial, bounds, fun_target, num_iter, seed)
    else:
        raise ValueError

    return X, Y


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--structure', type=str, required=True)
    parser.add_argument('--ind_materials', type=int, required=True)
    parser.add_argument('--fidelity', type=str, required=True)
    parser.add_argument('--property', type=str, required=True)
    parser.add_argument('--algorithm', type=str, required=True)
    parser.add_argument('--discrete', action='store_true')
    parser.add_argument('--ind_round', type=int, required=True)

    args = parser.parse_args()

    str_structure = args.structure
    ind_materials = args.ind_materials
    str_fidelity = args.fidelity
    str_property = args.property
    str_algorithm = args.algorithm
    is_discrete = args.discrete
    ind_round = args.ind_round

    num_rounds = 50
    num_iter = 1000
    seed = 42

    assert str_structure in [
        'threelayers2d',
        'threelayers3d',
        'nanocones2d',
        'nanocones3d',
        'nanospheres2d',
        'nanospheres3d',
        'nanowires2d',
        'nanowires3d',
        'doublenanocones2d',
        'doublenanocones3d',
    ]
    assert str_fidelity in ['low', 'medium', 'high']
    assert str_property in ['transmittance', 'reflectance', 'absorbance']
    assert str_algorithm in ['pybobyqa', 'powell', 'de', 'direct', 'bo', 'rs']

    _, _, size_mesh, materials = utils_structures.get_structure(
        str_structure, ind_materials, str_fidelity)
    bounds = utils_structures.get_bounds(str_structure)
    size_mesh /= constants.unit_length

    str_materials = '_'.join(materials)

    str_model = f'model_{str_structure}_{str_materials}_{size_mesh}_{str_property}.pt'
    str_dataset = f'dataset_{str_structure}_{str_materials}_{size_mesh}_{str_property}.npy'
    print(str_model, flush=True)
    print(str_dataset, flush=True)
    print(str_algorithm, flush=True)

    assert os.path.exists(os.path.join(path_trained_models, str_model))
    assert os.path.exists(os.path.join(path_trained_models, str_dataset))

    dict_dataset = np.load(os.path.join(path_trained_models, str_dataset), allow_pickle=True)
    dict_dataset = dict_dataset[()]

    if is_discrete:
        X_all = dict_dataset['X']
        by_all = dict_dataset['by']

        def fun_target(bx):
            return utils_optimization.evaluate_discrete(bx, str_structure, X_all, by_all)
    else:
        X_test = dict_dataset['X_test']
        by_test = dict_dataset['by_test']

        print(X_test.shape, by_test.shape, flush=True)
        print('', flush=True)

        dim_X = X_test.shape[1]

        dataloader_test = train_test.load_dataloader_test(X_test, by_test)
        model, criterion, _ = train_test.load_model_criterion_optimizer(dim_X)
        train_test.load_model(model, path_trained_models, str_model)
        loss_test, _ = train_test.test(model, criterion, dataloader_test)

        print(f'loss_test {loss_test:.4f}', flush=True)
        print('', flush=True)

        def fun_target(bx):
            return utils_optimization.evaluate_continuous(bx, str_structure, model)

    X_initial = np.random.RandomState(seed).uniform(size=(num_rounds, bounds.shape[0]))
    X_initial = (bounds[:, 1] - bounds[:, 0]) * X_initial + bounds[:, 0]
    print(X_initial.shape)

    bx_initial = X_initial[ind_round]
    print(f'Round {ind_round+1}', flush=True)
    X, Y = run_algorithm(str_algorithm, bx_initial, bounds, fun_target, num_iter, ind_round)

    dict_all = {
        'str_structure': str_structure,
        'ind_materials': ind_materials,
        'str_fidelity': str_fidelity,
        'str_property': str_property,
        'str_algorithm': str_algorithm,
        'str_materials': str_materials,
        'str_model': str_model,
        'str_dataset': str_dataset,
        'num_rounds': num_rounds,
        'num_iter': num_iter,
        'ind_round': ind_round,
        'seed': seed,
        'X': X,
        'Y': Y,
    }

    if not os.path.exists(path_optimization_results):
        os.mkdir(path_optimization_results)

    str_file = os.path.join(path_optimization_results, f'results_{str_structure}_{str_materials}_{size_mesh}_{str_property}_{str_algorithm}_{num_iter}_{ind_round}.npy')
    np.save(str_file, dict_all)
