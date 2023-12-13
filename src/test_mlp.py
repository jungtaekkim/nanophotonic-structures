import numpy as np
import os

from nanophotonic_structures.surrogates import train_test

import constants as constants_src


path_trained_models = constants_src.path_trained_models


if __name__ == '__main__':
    str_files = os.listdir(path_trained_models)
    str_files.sort()

    for str_file in str_files:
        print(str_file, flush=True)
        list_str_file = str_file.split('_')

        if list_str_file[0] == 'model':
            str_dataset = '_'.join(['dataset'] + list_str_file[1:])[:-3] + '.npy'
            print(str_dataset, flush=True)
            print('', flush=True)

            dict_dataset = np.load(os.path.join(path_trained_models, str_dataset), allow_pickle=True)
            dict_dataset = dict_dataset[()]

            X_train = dict_dataset['X_train']
            by_train = dict_dataset['by_train']
            X_valid = dict_dataset['X_valid']
            by_valid = dict_dataset['by_valid']
            X_test = dict_dataset['X_test']
            by_test = dict_dataset['by_test']

            print(X_train.shape, by_train.shape, flush=True)
            print(X_valid.shape, by_valid.shape, flush=True)
            print(X_test.shape, by_test.shape, flush=True)
            print('', flush=True)

            size_batch = 64

            dataloader_train, dataloader_valid, dataloader_test = train_test.load_dataloader(
                X_train, X_valid, X_test, by_train, by_valid, by_test, size_batch)

            dim_X = X_train.shape[1]

            model, criterion, _ = train_test.load_model_criterion_optimizer(dim_X)
            train_test.load_model(model, path_trained_models, str_file)

            loss_train, _ = train_test.test(model, criterion, dataloader_train)
            loss_valid, _ = train_test.test(model, criterion, dataloader_valid)
            loss_test, _ = train_test.test(model, criterion, dataloader_test)

            print(f'loss_train {loss_train:.4f}', flush=True)
            print(f'loss_valid {loss_valid:.4f}', flush=True)
            print(f'loss_test {loss_test:.4f}', flush=True)
            print(f'loss_test {loss_test:.6f}', flush=True)
            print('', flush=True)
