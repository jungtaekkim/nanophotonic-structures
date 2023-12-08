import numpy as np
import os
import csv
import scipy.interpolate as sciip


path_spectra = '../spectra'

def load_csv(str_file_csv, path_spectra=path_spectra):
    with open(os.path.join(path_spectra, str_file_csv)) as file_csv:
        reader_csv = csv.reader(file_csv, delimiter=',')

        data = []
        for row in reader_csv:
            data.append(row)

    data = np.array(data).astype(np.float64)
    return data

def get_model_interpolation(str_standard_illuminant, path_spectra=path_spectra):
    if str_standard_illuminant == 'C':
        str_file_csv = 'CIE_illum_C.csv'
    elif str_standard_illuminant == 'D50':
        str_file_csv = 'CIE_std_illum_D50.csv'
    elif str_standard_illuminant == 'D55':
        str_file_csv = 'CIE_illum_D55.csv'
    elif str_standard_illuminant == 'D65':
        str_file_csv = 'CIE_std_illum_D65.csv'
    elif str_standard_illuminant == 'D75':
        str_file_csv = 'CIE_illum_D75.csv'
    else:
        raise ValueError

    data = load_csv(str_file_csv, path_spectra=path_spectra)
    model_interpolation = sciip.interp1d(data[:, 0], data[:, 1], kind='linear')

    return model_interpolation

def compute_efficiency(wavelengths, values, intensities):
    assert len(wavelengths.shape) == 1
    assert len(values.shape) == 1
    assert len(intensities.shape) == 1
    assert wavelengths.shape[0] == values.shape[0]
    assert intensities.shape[0] == values.shape[0]

    indices = np.argsort(wavelengths)

    wavelengths = wavelengths[indices]
    values = values[indices]
    intensities = intensities[indices]

    intensities_ = intensities * values

    numerator = (0.5 * (intensities_[1:] + intensities_[:-1])) * (wavelengths[1:] - wavelengths[:-1])
    denominator = (0.5 * (intensities[1:] + intensities[:-1])) * (wavelengths[1:] - wavelengths[:-1])

    indices_not_zero = denominator != 0
    numerator = numerator[indices_not_zero]
    denominator = denominator[indices_not_zero]

    efficiency = np.mean(numerator / denominator)

    return efficiency

def compute_efficiencies(wavelengths, values, str_standard_illuminant='D65'):
    assert len(wavelengths.shape) == 1
    assert wavelengths.shape[0] == values.shape[-1]
    assert str_standard_illuminant in ['C', 'D50', 'D55', 'D65', 'D75']

    model_interpolation = get_model_interpolation(str_standard_illuminant)
    intensities = model_interpolation(wavelengths)

    shape_values = values.shape
    if len(shape_values) > 2:
        values = np.reshape(
            values,
            (-1, shape_values[-1]),
            order='C'
        )

    new_values = []
    for elem in values:
        new_values.append(compute_efficiency(wavelengths, elem, intensities))
    values = np.array(new_values)

    if len(shape_values) > 2:
        values = np.reshape(
            values,
            shape_values[:-1],
            order='C'
        )

    return values


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    data_c = load_csv('CIE_illum_C.csv', path_spectra='../../spectra')
    data_d50 = load_csv('CIE_std_illum_D50.csv', path_spectra='../../spectra')
    data_d55 = load_csv('CIE_illum_D55.csv', path_spectra='../../spectra')
    data_d65 = load_csv('CIE_std_illum_D65.csv', path_spectra='../../spectra')
    data_d75 = load_csv('CIE_illum_D75.csv', path_spectra='../../spectra')

    model_interpolation_c = get_model_interpolation('C', path_spectra='../../spectra')
    model_interpolation_d50 = get_model_interpolation('D50', path_spectra='../../spectra')
    model_interpolation_d55 = get_model_interpolation('D55', path_spectra='../../spectra')
    model_interpolation_d65 = get_model_interpolation('D65', path_spectra='../../spectra')
    model_interpolation_d75 = get_model_interpolation('D75', path_spectra='../../spectra')

    bx = np.linspace(380, 750, 10000)

    plt.plot(data_c[:, 0], data_c[:, 1], label='C')
    plt.plot(data_d50[:, 0], data_d50[:, 1], label='D50')
    plt.plot(data_d55[:, 0], data_d55[:, 1], label='D55')
    plt.plot(data_d65[:, 0], data_d65[:, 1], label='D65')
    plt.plot(data_d75[:, 0], data_d75[:, 1], label='D75')

    plt.plot(bx, model_interpolation_c(bx), label='C (interpolated)')
    plt.plot(bx, model_interpolation_d50(bx), label='D50 (interpolated)')
    plt.plot(bx, model_interpolation_d55(bx), label='D55 (interpolated)')
    plt.plot(bx, model_interpolation_d65(bx), label='D65 (interpolated)')
    plt.plot(bx, model_interpolation_d75(bx), label='D75 (interpolated)')

    plt.grid()
    plt.legend()
    plt.show()
