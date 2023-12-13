import numpy as np

from nanophotonic_structures.surrogates import train_test
from nanophotonic_structures.utils import utils_properties
from nanophotonic_structures.utils import utils_structures
from nanophotonic_structures.utils import utils_solar
from nanophotonic_structures.utils import utils_standardilluminant


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

def evaluate_direct(bx, str_structure, ind_materials, str_fidelity, str_property):
    assert isinstance(str_structure, str)
    assert isinstance(ind_materials, int)
    assert isinstance(str_fidelity, str)
    assert isinstance(str_property, str)
    assert len(bx.shape) == 1

    target_class, depth_pml, size_mesh, materials = utils_structures.get_structure(
        str_structure, ind_materials, str_fidelity)

    obj = target_class(
        depth_pml=depth_pml,
        size_mesh=size_mesh,
        mode='decay',
        materials=materials,
        show_figures=False,
        save_figures=False,
        save_properties=False,
        save_efields_hfields=False,
    )

    dict_all = obj.run(bx)
    wavelengths = dict_all['wavelengths']
    values = np.array([dict_all[str_property]])

    if str_structure in ['threelayers2d', 'threelayers3d']:
        multiplier = -1.0
        value = values[0, 0]
    elif str_structure in ['nanocones2d', 'nanocones3d']:
        multiplier = 1.0
        value = utils_solar.compute_efficiencies(wavelengths, values, [])[0]
    elif str_structure in ['nanowires2d', 'nanowires3d', 'nanospheres2d', 'nanospheres3d']:
        multiplier = -1.0
        value = utils_solar.compute_efficiencies(wavelengths, values, materials)[0]
    elif str_structure in ['doublenanocones2d', 'doublenanocones3d']:
        multiplier = -1.0
        value = utils_standardilluminant.compute_efficiencies(wavelengths, values)[0]
    else:
        raise ValueError

    return multiplier * value
