import numpy as np
import argparse
import os

from nanophotonic_structures.utils import utils_structures


skip_experiment = True


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--structure', type=str, required=True)
    parser.add_argument('--ind_materials', type=int, required=True)
    parser.add_argument('--fidelity', type=str, required=True)
    parser.add_argument('--num_chunks', type=int, required=True)
    parser.add_argument('--ind_chunk', type=int, required=True)

    args = parser.parse_args()

    str_structure = args.structure
    ind_materials = args.ind_materials
    str_fidelity = args.fidelity
    num_chunks = args.num_chunks
    ind_chunk = args.ind_chunk

    assert str_structure in [
        'doublenanocones2d',
        'doublenanocones3d',
        'threelayers2d',
        'threelayers3d',
        'nanocones2d',
        'nanocones3d',
        'nanospheres2d',
        'nanospheres3d',
        'nanowires2d',
        'nanowires3d',
    ]
    assert str_fidelity in ['low', 'medium', 'high']
    assert ind_chunk < num_chunks

    target_class, depth_pml, size_mesh, materials = utils_structures.get_structure(
        str_structure, ind_materials, str_fidelity)
    bounds = utils_structures.get_bounds(str_structure)
    grids = utils_structures.get_grids(str_structure, bounds)

    size_chunk = grids.shape[0] // num_chunks
    if grids.shape[0] % num_chunks != 0:
        size_chunk += 1

    grids = grids[ind_chunk * size_chunk:(ind_chunk + 1) * size_chunk]

    for variables in grids:
        try:
            obj = target_class(
                depth_pml=depth_pml,
                size_mesh=size_mesh,
                mode='decay',
                materials=materials,
                save_properties=True,
            )

            variables = np.array(variables)
            print('variables')
            print(variables)

            if skip_experiment:
                path_current = obj.get_path_current()
                str_file = obj.get_str_file(obj.transform(variables))

                if os.path.exists(os.path.join(path_current, str_file)):
                    print('passed')
                    continue

            obj.run(variables)
        except:
            pass
