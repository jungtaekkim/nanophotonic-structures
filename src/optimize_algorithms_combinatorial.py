import numpy as np
import argparse
import os

from nanophotonic_structures import constants
from nanophotonic_structures.utils import utils_solar

from nanophotonic_structures.combinatorial_2d import Combinatorial2D

import baselines_combinatorial.random_search as random_search

import constants as constants_src


path_optimization_results = constants_src.path_optimization_results

num_materials = 12


def run_algorithm(str_algorithm, bx_initial, bounds, fun_target, num_iter, seed):
    if str_algorithm == 'rs':
        X, Y = random_search.random_search(bx_initial, bounds, num_materials, fun_target, num_iter, seed)
    else:
        raise ValueError

    return X, Y


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--structure', type=str, required=True)
    parser.add_argument('--fidelity', type=str, required=True)
    parser.add_argument('--property', type=str, required=True)
    parser.add_argument('--algorithm', type=str, required=True)
    parser.add_argument('--ind_round', type=int, required=True)

    args = parser.parse_args()

    str_structure = args.structure
    str_fidelity = args.fidelity
    str_property = args.property
    str_algorithm = args.algorithm
    ind_round = args.ind_round

    num_rounds = 50
    num_iter = 100
    seed = 42

    assert str_structure in [
        'combinatorial2d',
        'combinatorial3d',
    ]
    assert str_fidelity in ['low', 'medium', 'high']
    assert str_property in ['transmittance', 'reflectance', 'absorbance']
    assert str_algorithm in ['rs']

    if str_structure == 'combinatorial2d':
        num_variables = 80
    else:
        raise ValueError

    bounds = np.array([
        [0, num_materials - 1],
    ] * num_variables)

    obj = Combinatorial2D(
        depth_pml=50,
        size_mesh=1,
        mode='decay',
        show_figures=False,
        save_figures=False,
        save_properties=False,
        save_efields_hfields=False,
    )
    size_mesh = obj.size_mesh
    str_materials = '_'.join(obj.list_materials)

    print('str_fidelity is dismissed now', flush=True)
    print(str_algorithm, flush=True)

    def fun_target(bx):
        dict_all = obj.run(bx)
        value = dict_all[str_property]
        wavelengths = dict_all['wavelengths']

        by = utils_solar.compute_efficiency(wavelengths, value, None)
        by *= -1.0

        return by

    X_initial = np.random.RandomState(seed).choice(num_materials, size=(num_rounds, bounds.shape[0]))
    print(X_initial.shape)

    bx_initial = X_initial[ind_round]
    print(f'Round {ind_round+1}', flush=True)
    X, Y = run_algorithm(str_algorithm, bx_initial, bounds, fun_target, num_iter, ind_round)

    dict_all = {
        'str_structure': str_structure,
        'str_fidelity': str_fidelity,
        'str_property': str_property,
        'str_algorithm': str_algorithm,
        'str_materials': str_materials,
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
