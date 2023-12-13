import numpy as np
import os
import h5py
import torch
import sklearn.model_selection as sklms

from nanophotonic_structures import constants
from nanophotonic_structures.surrogates import model_mlp
from nanophotonic_structures.surrogates import dataset
from nanophotonic_structures.utils import utils_structures
from nanophotonic_structures.utils import utils_solar
from nanophotonic_structures.utils import utils_standardilluminant


def random_seed():
    torch.manual_seed(42)
    np.random.seed(42)

def load_dataset(path_collected_datasets, str_structure, ind_materials, str_fidelity, str_property):
    _, _, size_mesh, materials = utils_structures.get_structure(
        str_structure, ind_materials, str_fidelity)
    str_materials = '_'.join(materials)

    size_mesh /= constants.unit_length

    str_variables = f'{str_structure}_{str_materials}_{size_mesh}_variables.h5'
    str_wavelengths = f'{str_structure}_{str_materials}_{size_mesh}_wavelengths.h5'
    str_file = f'{str_structure}_{str_materials}_{size_mesh}_{str_property}.h5'
    print(f'{os.path.join(path_collected_datasets, str_file)}')

    variables = np.array(h5py.File(os.path.join(path_collected_datasets, str_variables), 'r')['data'])
    wavelengths = np.array(h5py.File(os.path.join(path_collected_datasets, str_wavelengths), 'r')['data'])
    values = np.array(h5py.File(os.path.join(path_collected_datasets, str_file), 'r')['data'])

    assert len(variables.shape) == 3 or len(variables.shape) == 4 or len(variables.shape) == 8
    assert len(values.shape) == 3 or len(values.shape) == 4 or len(values.shape) == 8
    assert variables.shape[0] == values.shape[0]
    assert variables.shape[1] == values.shape[1]

    if len(variables.shape) == 4:
        assert variables.shape[2] == values.shape[2]

    if len(variables.shape) == 8:
        assert variables.shape[2] == values.shape[2]
        assert variables.shape[3] == values.shape[3]
        assert variables.shape[4] == values.shape[4]
        assert variables.shape[5] == values.shape[5]
        assert variables.shape[6] == values.shape[6]

    return variables, wavelengths, values, str_materials, size_mesh, materials

def convert_dataset(variables, wavelengths, values, materials, str_structure):
    X = np.reshape(
        variables,
        (-1, variables.shape[-1]),
        order='C'
    )

    Y = np.reshape(
        values,
        (-1, values.shape[-1]),
        order='C'
    )

    if Y.shape[1] == 1:
        by = Y[:, 0]
    elif Y.shape[1] == 4000:
        assert Y.shape[1] == wavelengths.shape[0]
        assert str_structure in ['nanocones2d', 'nanocones3d', 'nanowires2d', 'nanowires3d', 'nanospheres2d', 'nanospheres3d']

        by = utils_solar.compute_efficiencies(wavelengths, Y, materials)
    elif Y.shape[1] == 500:
        assert Y.shape[1] == wavelengths.shape[0]
        assert str_structure in ['doublenanocones2d', 'doublenanocones3d']

        by = utils_standardilluminant.compute_efficiencies(wavelengths, Y)
    else:
        raise ValueError

    X = X.astype(np.float32)
    Y = Y.astype(np.float32)
    by = by.astype(np.float32)

    assert np.all(0 <= by) and np.all(by <= 1)

    return X, by

def split_dataset(X, by):
    test_size = 0.2
    valid_size = 0.1 / (1.0 - test_size)

    X_train, X_test, by_train, by_test = sklms.train_test_split(X, by, test_size=test_size, random_state=42)
    X_train, X_valid, by_train, by_valid = sklms.train_test_split(X_train, by_train, test_size=valid_size, random_state=42 * 2)

    return X_train, X_valid, X_test, by_train, by_valid, by_test

def load_dataloader(X_train, X_valid, X_test, by_train, by_valid, by_test, size_batch):
    dataset_train = dataset.Dataset(X_train, by_train)
    dataset_valid = dataset.Dataset(X_valid, by_valid)
    dataset_test = dataset.Dataset(X_test, by_test)

    dataloader_train = torch.utils.data.DataLoader(dataset_train, batch_size=size_batch, shuffle=True)
    dataloader_valid = torch.utils.data.DataLoader(dataset_valid, batch_size=size_batch, shuffle=False)
    dataloader_test = torch.utils.data.DataLoader(dataset_test, batch_size=size_batch, shuffle=False)

    return dataloader_train, dataloader_valid, dataloader_test

def load_dataloader_test(X_test, by_test, size_batch=64):
    dataset_test = dataset.Dataset(X_test, by_test)
    dataloader_test = torch.utils.data.DataLoader(dataset_test, batch_size=size_batch, shuffle=False)

    return dataloader_test

def load_model_criterion_optimizer(dim_X):
    model = model_mlp.MLP(dim_X)
    criterion = torch.nn.MSELoss(reduction='mean')
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    return model, criterion, optimizer

def train(model, optimizer, criterion, dataloader_train):
    loss_train = 0.0
    count_train = 0

    model.train()

    for X_batch, by_batch in dataloader_train:
        optimizer.zero_grad()

        outputs = model(X_batch)
        loss = criterion(outputs, by_batch)
        loss.backward()
        optimizer.step()

        loss_train += loss.item() * X_batch.shape[0]
        count_train += X_batch.shape[0]

    loss_train /= count_train
    return loss_train, count_train

def test(model, criterion, dataloader_test):
    loss_test = 0.0
    count_test = 0

    model.eval()

    with torch.no_grad():
        for X_batch, by_batch in dataloader_test:
            outputs = model(X_batch)
            loss = criterion(outputs, by_batch)

            loss_test += loss.item() * X_batch.shape[0]
            count_test += X_batch.shape[0]

    loss_test /= count_test
    return loss_test, count_test

def predict(model, bx):
    assert isinstance(bx, np.ndarray)
    assert len(bx.shape) == 1

    bx = bx.astype(np.float32)

    model.eval()

    with torch.no_grad():
        outputs = model(torch.tensor(bx[np.newaxis, ...]))
        outputs = outputs.numpy()[0]

    return outputs

def train_validate(model, optimizer, criterion, dataloader_train, dataloader_valid, num_train, num_valid):
    num_epochs = 200
    size_window = 5

    list_loss_valid = []

    for ind_epoch in range(0, num_epochs):
        loss_train, count_train = train(model, optimizer, criterion, dataloader_train)
        loss_valid, count_valid = test(model, criterion, dataloader_valid)

        assert count_train == num_train
        assert count_valid == num_valid

        print(f'Epoch {ind_epoch+1}:')
        print(f'loss_train {loss_train:.4f} loss_valid {loss_valid:.4f}')

        list_loss_valid.append(loss_valid)
        mean_loss_valid = np.mean(list_loss_valid[-1 - size_window:-1])

        if (ind_epoch + 1) > 20 and mean_loss_valid < loss_valid:
            print('')
            print(f'mean_loss_valid {mean_loss_valid} < loss_valid {loss_valid}')
            print('loss_valid increases.')
            print('')
            break

def save_model(
    model, X, X_train, X_valid, X_test, by, by_train, by_valid, by_test,
    path_trained_models, str_structure, str_materials, size_mesh, str_property
):
    str_model = f'model_{str_structure}_{str_materials}_{size_mesh}_{str_property}.pt'
    torch.save(model.state_dict(), os.path.join(path_trained_models, str_model))

    dict_dataset = {
        'X': X,
        'by': by,
        'X_train': X_train,
        'by_train': by_train,
        'X_valid': X_valid,
        'by_valid': by_valid,
        'X_test': X_test,
        'by_test': by_test,
    }
    str_dataset = f'dataset_{str_structure}_{str_materials}_{size_mesh}_{str_property}.npy'
    np.save(os.path.join(path_trained_models, str_dataset), dict_dataset)

def load_model(model, path_trained_models, str_file):
    model.load_state_dict(torch.load(os.path.join(path_trained_models, str_file)))
