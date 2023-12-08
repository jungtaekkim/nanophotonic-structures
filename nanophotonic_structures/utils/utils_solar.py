import numpy as np
import pvlib.spectrum as pvs


def compute_efficiency(wavelengths, values, str_material=None):
    assert len(wavelengths.shape) == 1
    assert len(values.shape) == 1
    assert wavelengths.shape[0] == values.shape[0]

    if str_material is None:
        cutoff_wavelength = np.inf
    elif str_material == 'cSi':
        cutoff_wavelength = 1107
    elif str_material == 'GaAs':
        cutoff_wavelength = 867
    elif str_material == 'CH3NH3PbI3':
        cutoff_wavelength = 821
    else:
        raise ValueError

    indices = np.argsort(wavelengths)

    wavelengths = wavelengths[indices]
    values = values[indices]

    values[wavelengths > cutoff_wavelength] = 0.0

    am15g = pvs.get_am15g(wavelengths).to_numpy()
    am15g_ = am15g * values

    numerator = (0.5 * (am15g_[1:] + am15g_[:-1])) * (wavelengths[1:] - wavelengths[:-1])
    denominator = (0.5 * (am15g[1:] + am15g[:-1])) * (wavelengths[1:] - wavelengths[:-1])

    indices_not_zero = denominator != 0
    numerator = numerator[indices_not_zero]
    denominator = denominator[indices_not_zero]

    efficiency = np.mean(numerator / denominator)

    return efficiency

def compute_efficiencies(wavelengths, values, materials):
    assert len(wavelengths.shape) == 1
    assert wavelengths.shape[0] == values.shape[-1]

    if 'cSi' in materials:
        str_mat = 'cSi'
    elif 'GaAs' in materials:
        str_mat = 'GaAs'
    elif 'CH3NH3PbI3' in materials:
        str_mat = 'CH3NH3PbI3'
    elif 'methylammonium_lead_iodide' in materials:
        str_mat = 'CH3NH3PbI3'
    else:
        str_mat = None

    shape_values = values.shape
    if len(shape_values) > 2:
        values = np.reshape(
            values,
            (-1, shape_values[-1]),
            order='C'
        )

    new_values = []
    for elem in values:
        new_values.append(compute_efficiency(wavelengths, elem, str_mat))
    values = np.array(new_values)

    if len(shape_values) > 2:
        values = np.reshape(
            values,
            shape_values[:-1],
            order='C'
        )

    return values
