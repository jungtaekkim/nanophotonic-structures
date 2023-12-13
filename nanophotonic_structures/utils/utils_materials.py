import math
import meep as mp

import nanophotonic_structures.materials_meep as mtr_meep
import nanophotonic_structures.materials_custom as mtr_custom


def get_medium(frequency, part_real, part_imaginary):
    material = mp.Medium(epsilon=part_real, D_conductivity=2 * math.pi * frequency * part_imaginary / part_real)

    return material

def get_material(str_material):
    if str_material in ['Ag', 'silver']:
        material = mtr_meep.Ag
    elif str_material in ['Au']:
        material = mtr_meep.Au
    elif str_material in ['Cu']:
        material = mtr_meep.Cu
    elif str_material in ['Ni']:
        material = mtr_meep.Ni
    elif str_material in ['aSi']:
        material = mtr_custom.aSi
    elif str_material in ['cSi']:
        material = mtr_custom.cSi
    elif str_material in ['GaAs']:
        material = mtr_custom.GaAs
    elif str_material in ['TiO2']:
        material = mtr_custom.TiO2
    elif str_material in ['ZnO']:
        material = mtr_custom.ZnO
    elif str_material in ['ITO']:
        material = mtr_custom.ITO
    elif str_material in ['AZO']:
        material = mtr_custom.AZO
    elif str_material in ['CH3NH3PbI3', 'methylammonium_lead_iodide']:
        material = mtr_custom.CH3NH3PbI3
    elif str_material in ['fusedsilica']:
        material = mtr_custom.fusedsilica
    elif str_material in ['air', 'Air']:
        part_real = 1.0

        material = mp.Medium(epsilon=part_real)
    elif str_material in ['test_1.8']:
        part_real = 1.8

        material = mp.Medium(epsilon=part_real)
    elif str_material in ['test_2.4']:
        part_real = 2.4

        material = mp.Medium(epsilon=part_real)
    elif str_material in ['test_6.25']:
        part_real = 6.25

        material = mp.Medium(epsilon=part_real)
    else:
        raise ValueError

    return material
