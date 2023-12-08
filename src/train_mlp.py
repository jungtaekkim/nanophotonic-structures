import os
import argparse

from nanophotonic_structures.surrogates import train_test

import constants as constants_src


path_collected_datasets = constants_src.path_collected_datasets
path_trained_models = constants_src.path_trained_models


if __name__ == '__main__':
    assert os.path.exists(path_trained_models)
    train_test.random_seed()

    parser = argparse.ArgumentParser()
    parser.add_argument('--structure', type=str, required=True)
    parser.add_argument('--ind_materials', type=int, required=True)
    parser.add_argument('--fidelity', type=str, required=True)
    parser.add_argument('--property', type=str, required=True)

    args = parser.parse_args()

    str_structure = args.structure
    ind_materials = args.ind_materials
    str_fidelity = args.fidelity
    str_property = args.property

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

    variables, wavelengths, values, str_materials, size_mesh, materials = train_test.load_dataset(
        path_collected_datasets, str_structure, ind_materials, str_fidelity, str_property)

    print(variables.shape, flush=True)
    print(wavelengths.shape, flush=True)
    print(values.shape, flush=True)

    if str_structure in [
        'threelayers2d',
        'threelayers3d',
        'nanocones2d',
        'nanocones3d',
        'doublenanocones2d',
        'doublenanocones3d',
    ]:
        materials = []

    X, by = train_test.convert_dataset(variables, wavelengths, values, materials, str_structure)
    X_train, X_valid, X_test, by_train, by_valid, by_test = train_test.split_dataset(X, by)

    print(X_train.shape, by_train.shape, flush=True)
    print(X_valid.shape, by_valid.shape, flush=True)
    print(X_test.shape, by_test.shape, flush=True)

    print(X_train.dtype, by_train.dtype, flush=True)
    print(X_valid.dtype, by_valid.dtype, flush=True)
    print(X_test.dtype, by_test.dtype, flush=True)

    size_batch = 64

    dim_X = X_train.shape[1]
    num_train = X_train.shape[0]
    num_valid = X_valid.shape[0]
    num_test = X_test.shape[0]

    dataloader_train, dataloader_valid, dataloader_test = train_test.load_dataloader(
        X_train, X_valid, X_test, by_train, by_valid, by_test, size_batch)
    model, criterion, optimizer = train_test.load_model_criterion_optimizer(dim_X)

    train_test.train_validate(model, optimizer, criterion, dataloader_train, dataloader_valid, num_train, num_valid)

    loss_train, _ = train_test.test(model, criterion, dataloader_train)
    loss_valid, _ = train_test.test(model, criterion, dataloader_valid)
    loss_test, _ = train_test.test(model, criterion, dataloader_test)

    print('', flush=True)
    print(f'loss_train {loss_train:.4f}', flush=True)
    print(f'loss_valid {loss_valid:.4f}', flush=True)
    print(f'loss_test {loss_test:.4f}', flush=True)
    print('', flush=True)

    train_test.save_model(model, X, X_train, X_valid, X_test, by, by_train, by_valid, by_test,
        path_trained_models, str_structure, str_materials, size_mesh, str_property)
