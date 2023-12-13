import numpy as np


unit_length = 10

wavelength_default = 550
wavelength_solar = (280, 2500)
wavelength_visible = (380, 750)

num_wavelengths_solar = 4000
num_wavelengths_visible = 500

##
bounds_doublenanocones = np.array([
    [10, 50], # thickness first
    [3, 20], # thickness second
    [10, 50], # thickness third
    [20, 50], # radius first
    [50, 100], # height first
    [20, 50], # radius second
    [50, 100], # height second
])
depth_pml_doublenanocones = 50

size_mesh_doublenanocones2d_low = 20
size_mesh_doublenanocones2d_medium = 10
size_mesh_doublenanocones2d_high = 1

size_mesh_doublenanocones3d_low = 20
size_mesh_doublenanocones3d_medium = 10
size_mesh_doublenanocones3d_high = 1

materials_doublenanocones = [
    ['TiO2', 'Ag', 'TiO2', 'TiO2', 'TiO2'],
    ['TiO2', 'Au', 'TiO2', 'TiO2', 'TiO2'],
    ['TiO2', 'Cu', 'TiO2', 'TiO2', 'TiO2'],
    ['TiO2', 'Ni', 'TiO2', 'TiO2', 'TiO2'],
    ['cSi', 'Ag', 'cSi', 'cSi', 'cSi'],
    ['ZnO', 'Ag', 'ZnO', 'ZnO', 'ZnO'],
    ['ITO', 'Ag', 'ITO', 'ITO', 'ITO'],
    ['AZO', 'Ag', 'AZO', 'AZO', 'AZO'],
]

##
bounds_nanocones = np.array([
    [5, 150], # radius
    [1, 300], # height
])
depth_pml_nanocones = 50

size_mesh_nanocones2d_low = 20
size_mesh_nanocones2d_medium = 10
size_mesh_nanocones2d_high = 1

size_mesh_nanocones3d_low = 20
size_mesh_nanocones3d_medium = 10
size_mesh_nanocones3d_high = 1

materials_nanocones = [
    ['fusedsilica', 'fusedsilica'],
]

##
bounds_nanowires = np.array([
    [1, 200], # pitch - 2 radius
    [5, 200], # radius
    [200, 200], # height
])
depth_pml_nanowires = 50

size_mesh_nanowires2d_low = 20
size_mesh_nanowires2d_medium = 10
size_mesh_nanowires2d_high = 1

size_mesh_nanowires3d_low = 20
size_mesh_nanowires3d_medium = 10
size_mesh_nanowires3d_high = 1

materials_nanowires = [
    ['cSi'],
    ['GaAs'],
    ['CH3NH3PbI3'],
]

##
bounds_nanospheres = np.array([
    [100, 400], # thickness
    [10, 200], # radius
])
depth_pml_nanospheres = 50

size_mesh_nanospheres2d_low = 20
size_mesh_nanospheres2d_medium = 10
size_mesh_nanospheres2d_high = 1

size_mesh_nanospheres3d_low = 20
size_mesh_nanospheres3d_medium = 10
size_mesh_nanospheres3d_high = 1

materials_nanospheres = [
    ['cSi', 'TiO2'],
    ['GaAs', 'TiO2'],
    ['CH3NH3PbI3', 'TiO2'],
]

##
bounds_threelayers = np.array([
    [10, 100], # thickness first
    [3, 20], # thickness second
    [10, 100], # thickness third
])
depth_pml_threelayers = 50

size_mesh_threelayers2d_low = 20
size_mesh_threelayers2d_medium = 10
size_mesh_threelayers2d_high = 1

size_mesh_threelayers3d_low = 20
size_mesh_threelayers3d_medium = 10
size_mesh_threelayers3d_high = 1

materials_threelayers = [
    ['TiO2', 'Ag', 'TiO2'],
    ['TiO2', 'Au', 'TiO2'],
    ['TiO2', 'Cu', 'TiO2'],
    ['TiO2', 'Ni', 'TiO2'],
    ['cSi', 'Ag', 'cSi'],
    ['ZnO', 'Ag', 'ZnO'],
    ['ITO', 'Ag', 'ITO'],
    ['AZO', 'Ag', 'AZO'],
]
