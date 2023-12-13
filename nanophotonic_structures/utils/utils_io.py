import numpy as np
import os
import matplotlib.pyplot as plt


def get_str_figures(str_prefix, path_figures='../figures'):
    if not os.path.exists(path_figures):
        os.mkdir(path_figures)

    str_structure_empty = f'{str_prefix}_structure_empty.png'
    str_structure = f'{str_prefix}_structure.png'
    str_efield_z = f'{str_prefix}_efield_z.png'
    str_hfield_z = f'{str_prefix}_hfield_z.png'

    str_structure_empty = os.path.join(path_figures, str_structure_empty)
    str_structure = os.path.join(path_figures, str_structure)
    str_efield_z = os.path.join(path_figures, str_efield_z)
    str_hfield_z = os.path.join(path_figures, str_hfield_z)

    return str_structure_empty, str_structure, str_efield_z, str_hfield_z

def visualize_3d(epsilons, use_edgecolor=False):
    assert isinstance(epsilons, np.ndarray)
    assert len(epsilons.shape) == 3

    epsilons[epsilons == 1.0] = 0.0

    if np.max(epsilons) != np.min(epsilons):
        epsilons = (epsilons - np.min(epsilons)) / (np.max(epsilons) - np.min(epsilons))

    colormap = plt.get_cmap('binary')
    colors = colormap(epsilons)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.voxels(epsilons, facecolors=colors, edgecolor='white' if use_edgecolor else None)

    plt.show()
