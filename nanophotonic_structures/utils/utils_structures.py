import numpy as np
import itertools

from nanophotonic_structures.doublenanocones_2d import DoubleNanocones2D
from nanophotonic_structures.doublenanocones_3d import DoubleNanocones3D

from nanophotonic_structures.nanocones_2d import Nanocones2D
from nanophotonic_structures.nanocones_3d import Nanocones3D

from nanophotonic_structures.nanospheres_2d import Nanospheres2D
from nanophotonic_structures.nanospheres_3d import Nanospheres3D

from nanophotonic_structures.nanowires_2d import Nanowires2D
from nanophotonic_structures.nanowires_3d import Nanowires3D

from nanophotonic_structures.threelayers_2d import ThreeLayers2D
from nanophotonic_structures.threelayers_3d import ThreeLayers3D

from nanophotonic_structures import constants


def get_gap(str_structure):
    if str_structure in [
        'doublenanocones2d',
        'doublenanocones3d',
    ]:
        gap = 5
    else:
        gap = 1

    return gap

def get_grids_unfiltered(str_structure, bounds):
    gap = get_gap(str_structure)

    for bound in bounds:
        assert isinstance(bound[0], (int, np.int64))
        assert isinstance(bound[1], (int, np.int64))

    all_variables = [np.array(list(range(bound[0], bound[1] + 1, gap))) for bound in bounds]
    grids = list(itertools.product(*all_variables))

    return np.array(grids), all_variables

def get_grids(str_structure, bounds):
    grids, _ = get_grids_unfiltered(str_structure, bounds)
    new_grids = []

    for variables in grids:
        if str_structure in []:
            pass

        new_grids.append(variables)

    return np.array(new_grids)

def get_bounds(str_structure):
    if str_structure in [
        'doublenanocones2d',
        'doublenanocones3d',
    ]:
        bounds = constants.bounds_doublenanocones
    elif str_structure in [
        'nanocones2d',
        'nanocones3d',
    ]:
        bounds = constants.bounds_nanocones
    elif str_structure in [
        'nanospheres2d',
        'nanospheres3d',
    ]:
        bounds = constants.bounds_nanospheres
    elif str_structure in [
        'nanowires2d',
        'nanowires3d',
    ]:
        bounds = constants.bounds_nanowires
    elif str_structure in [
        'threelayers2d',
        'threelayers3d',
    ]:
        bounds = constants.bounds_threelayers
    else:
        raise ValueError

    return bounds

def get_structure(str_structure, index_materials, fidelity):
    assert index_materials >= 0
    assert fidelity in ['low', 'medium', 'high']

    if str_structure == 'doublenanocones2d':
        assert index_materials < len(constants.materials_doublenanocones)

        target_class = DoubleNanocones2D

        depth_pml = constants.depth_pml_doublenanocones

        if fidelity == 'low':
            size_mesh = constants.size_mesh_doublenanocones2d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_doublenanocones2d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_doublenanocones2d_high
        else:
            raise ValueError

        materials = constants.materials_doublenanocones[index_materials]
    elif str_structure == 'doublenanocones3d':
        assert index_materials < len(constants.materials_doublenanocones)

        target_class = DoubleNanocones3D

        depth_pml = constants.depth_pml_doublenanocones

        if fidelity == 'low':
            size_mesh = constants.size_mesh_doublenanocones3d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_doublenanocones3d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_doublenanocones3d_high
        else:
            raise ValueError

        materials = constants.materials_doublenanocones[index_materials]
    elif str_structure == 'nanocones2d':
        assert index_materials < len(constants.materials_nanocones)

        target_class = Nanocones2D

        depth_pml = constants.depth_pml_nanocones

        if fidelity == 'low':
            size_mesh = constants.size_mesh_nanocones2d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_nanocones2d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_nanocones2d_high
        else:
            raise ValueError

        materials = constants.materials_nanocones[index_materials]
    elif str_structure == 'nanocones3d':
        assert index_materials < len(constants.materials_nanocones)

        target_class = Nanocones3D

        depth_pml = constants.depth_pml_nanocones

        if fidelity == 'low':
            size_mesh = constants.size_mesh_nanocones3d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_nanocones3d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_nanocones3d_high
        else:
            raise ValueError

        materials = constants.materials_nanocones[index_materials]
    elif str_structure == 'nanospheres2d':
        assert index_materials < len(constants.materials_nanospheres)

        target_class = Nanospheres2D

        depth_pml = constants.depth_pml_nanospheres

        if fidelity == 'low':
            size_mesh = constants.size_mesh_nanospheres2d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_nanospheres2d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_nanospheres2d_high
        else:
            raise ValueError

        materials = constants.materials_nanospheres[index_materials]
    elif str_structure == 'nanospheres3d':
        assert index_materials < len(constants.materials_nanospheres)

        target_class = Nanospheres3D

        depth_pml = constants.depth_pml_nanospheres

        if fidelity == 'low':
            size_mesh = constants.size_mesh_nanospheres3d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_nanospheres3d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_nanospheres3d_high
        else:
            raise ValueError

        materials = constants.materials_nanospheres[index_materials]
    elif str_structure == 'nanowires2d':
        assert index_materials < len(constants.materials_nanowires)

        target_class = Nanowires2D

        depth_pml = constants.depth_pml_nanowires

        if fidelity == 'low':
            size_mesh = constants.size_mesh_nanowires2d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_nanowires2d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_nanowires2d_high
        else:
            raise ValueError

        materials = constants.materials_nanowires[index_materials]
    elif str_structure == 'nanowires3d':
        assert index_materials < len(constants.materials_nanowires)

        target_class = Nanowires3D

        depth_pml = constants.depth_pml_nanowires

        if fidelity == 'low':
            size_mesh = constants.size_mesh_nanowires3d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_nanowires3d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_nanowires3d_high
        else:
            raise ValueError

        materials = constants.materials_nanowires[index_materials]
    elif str_structure == 'threelayers2d':
        assert index_materials < len(constants.materials_threelayers)

        target_class = ThreeLayers2D

        depth_pml = constants.depth_pml_threelayers

        if fidelity == 'low':
            size_mesh = constants.size_mesh_threelayers2d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_threelayers2d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_threelayers2d_high
        else:
            raise ValueError

        materials = constants.materials_threelayers[index_materials]
    elif str_structure == 'threelayers3d':
        assert index_materials < len(constants.materials_threelayers)

        target_class = ThreeLayers3D

        depth_pml = constants.depth_pml_threelayers

        if fidelity == 'low':
            size_mesh = constants.size_mesh_threelayers3d_low
        elif fidelity == 'medium':
            size_mesh = constants.size_mesh_threelayers3d_medium
        elif fidelity == 'high':
            size_mesh = constants.size_mesh_threelayers3d_high
        else:
            raise ValueError

        materials = constants.materials_threelayers[index_materials]
    else:
        raise ValueError

    return target_class, depth_pml, size_mesh, materials
