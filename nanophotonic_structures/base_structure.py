import os
import numpy as np
import time
import matplotlib.pyplot as plt
import abc
import meep as mp

from nanophotonic_structures import constants
from nanophotonic_structures.utils import utils_materials
from nanophotonic_structures.utils import utils_io


class BaseStructure(abc.ABC):
    def __init__(
        self,
        name, # a structure name
        mode, # a simulation mode, decay or fixed
        size_cell, # the size of a simulation cell
        depth_pml, # the depth of a PML layer
        size_mesh, # size_mesh
        materials, # list of materials
        show_figures, # a flag for showing figures
        save_figures, # a flag for saving figures
        save_properties, # a flag for saving properties
        save_efields_hfields, # a flag for saving E-fields and H-fields
        wavelength, # a wavelength, a single value of a tuple of min and max wavelengths
        eps_averaging=False, # a flag for eps_averaging
        time_step=2.0, # a time step
        path_outputs='../../outputs-nanophotonic-structures', # a path to save outputs
        path_properties='../../datasets-nanophotonic-structures', # a path to save properties
    ):
        # 1 = 10 nm
        self.unit_length = constants.unit_length
        assert self.unit_length == 10

        assert isinstance(name, str)
        assert isinstance(mode, str)
        assert isinstance(size_cell, (type(None), list))
        assert isinstance(depth_pml, int)
        assert isinstance(size_mesh, (int, float))
        assert isinstance(materials, list)
        assert isinstance(show_figures, bool)
        assert isinstance(save_figures, bool)
        assert isinstance(save_properties, bool)
        assert isinstance(save_efields_hfields, bool)
        assert isinstance(wavelength, (int, tuple))
        if isinstance(wavelength, tuple):
            assert len(wavelength) == 2
            assert isinstance(wavelength[0], int)
            assert isinstance(wavelength[1], int)
            assert wavelength[0] < wavelength[1]

            wavelength = (
                self.transform(wavelength[0]),
                self.transform(wavelength[1])
            )
        else:
            assert wavelength == 550

            wavelength = self.transform(wavelength)
        assert mode in ['decay', 'fixed'] # fixed is for testing.
        assert depth_pml == 50
        depth_pml = self.transform(depth_pml)

        if size_cell is None:
            self.use_fixed_size_cell = False
            size_cell = [np.inf, np.inf, np.inf]
        else:
            assert len(size_cell) == 3
            assert isinstance(size_cell[0], int)
            assert isinstance(size_cell[1], int)
            assert isinstance(size_cell[2], int)

            size_cell = [
                self.transform(size_cell[0]),
                self.transform(size_cell[1]),
                self.transform(size_cell[2])
            ]

            self.use_fixed_size_cell = True
            size_cell[1] = size_cell[1] + 2 * depth_pml

        size_mesh = self.transform(size_mesh)

        self.name = name
        self.mode = mode
        self.size_cell = size_cell
        self.depth_pml = depth_pml
        self.size_mesh = size_mesh
        self.resolution = 1 / size_mesh
        self.list_materials = materials
        self.show_figures = show_figures
        self.save_figures = save_figures
        self.save_properties = save_properties
        self.save_efields_hfields = save_efields_hfields
        self.wavelength = wavelength
        self.eps_averaging = eps_averaging
        self.time_step = time_step

        self.steps_for_decay = 50
        self.decay_by = 1e-3

        self.margin_structure = 0.95

        self.path_outputs = path_outputs
        self.path_properties = path_properties

    def print_separators(self):
        print('=' * 80, flush=True)

    def get_frequency_info(self):
        if isinstance(self.wavelength, (float, int)):
            f_cen = 1 / self.wavelength
            d_f = 0.1 * f_cen
            num_f = 1
        else:
            f_min = 1 / self.wavelength[1]
            f_max = 1 / self.wavelength[0]

            f_cen = 0.5 * (f_min + f_max)
            d_f = f_max - f_min

            if np.all(self.wavelength == (self.transform(280), self.transform(2500))):
                num_f = constants.num_wavelengths_solar
            elif np.all(self.wavelength == (self.transform(380), self.transform(750))):
                num_f = constants.num_wavelengths_visible
            else:
                num_f = constants.num_wavelengths_solar

        return f_cen, d_f, num_f

    def verify_general(self, variables):
        assert isinstance(self.size_cell, list)
        assert len(self.size_cell) == 3
        assert self.size_cell[0] != np.inf
        assert self.size_cell[1] != np.inf
        assert self.size_cell[2] != np.inf
        assert self.num_variables == len(self.labels)

    def verify(self, variables):
        self.verify_general(variables)
        self.verify_specific(variables)

    def define_cell(self):
        self.cell = mp.Vector3(*self.size_cell)

    def define_pml(self):
        self.pml = [mp.PML(
            thickness=self.depth_pml,
            direction=mp.Y,
        )]

    def define_sources(self):
        f_cen, d_f, _ = self.get_frequency_info()

        self.sources = [
            mp.EigenModeSource(
                mp.GaussianSource(
                    frequency=f_cen,
                    fwidth=d_f,
                    is_integrated=True
                ),
                direction=mp.Y,
                size=mp.Vector3(self.size_cell[0], 0, 0),
                center=mp.Vector3(0, -0.5 * (self.size_cell[1] - 2 * self.depth_pml), 0),
            )
        ]

    def define_materials(self):
        materials = []

        for mat in self.list_materials:
            materials.append(utils_materials.get_material(mat))

        self.materials = materials

    def define_monitors(self):
        self.monitor_reflection = mp.FluxRegion(
            size=mp.Vector3(self.size_cell[0], 0, 0),
            center=mp.Vector3(0, -0.5 * (self.size_cell[1] - 2 * self.depth_pml) + self.depth_pml, 0),
            direction=mp.Y,
        )

        self.monitor_transmision = mp.FluxRegion(
            size=mp.Vector3(self.size_cell[0], 0, 0),
            center=mp.Vector3(0, 0.5 * (self.size_cell[1] - 2 * self.depth_pml), 0),
            direction=mp.Y,
        )

    def define_simulations(self, variables):
        str_current_experiment = self.get_str_current_experiment_with_variables(variables)

        self.sim_empty = mp.Simulation(
            cell_size=self.cell,
            boundary_layers=self.pml,
            sources=self.sources,
            resolution=self.resolution,
            k_point=mp.Vector3(),
            eps_averaging=self.eps_averaging,
            filename_prefix=f'{str_current_experiment}_empty',
        )

        self.sim = mp.Simulation(
            cell_size=self.cell,
            boundary_layers=self.pml,
            geometry=self.geometries,
            sources=self.sources,
            resolution=self.resolution,
            k_point=mp.Vector3(),
            eps_averaging=self.eps_averaging,
            filename_prefix=f'{str_current_experiment}',
        )

    def add_fluxes(self):
        f_cen, d_f, num_f = self.get_frequency_info()

        if isinstance(self.wavelength, (float, int)):
            d_f = 0

        self.refl_empty = self.sim_empty.add_flux(f_cen, d_f, num_f, self.monitor_reflection)
        self.tran_empty = self.sim_empty.add_flux(f_cen, d_f, num_f, self.monitor_transmision)

        self.refl = self.sim.add_flux(f_cen, d_f, num_f, self.monitor_reflection)
        self.tran = self.sim.add_flux(f_cen, d_f, num_f, self.monitor_transmision)

    def define_experiment(self, variables):
        self.verify(variables)

        self.prefix_file = self.get_str_current_experiment_with_variables(variables)

        self.define_cell()
        self.define_pml()
        self.define_sources()
        self.define_materials()
        self.define_monitors()
        self.define_geometries(variables)
        self.define_simulations(variables)
        self.add_fluxes()

        self.point_to_measure = mp.Vector3(0, 0.5 * (self.size_cell[1] - 2 * self.depth_pml) - self.depth_pml, 0)

    def compute_properties(self, variables_original, variables, freq_refl, fluxes_tran_empty, fluxes_refl, fluxes_tran):
        assert isinstance(variables_original, np.ndarray)
        assert isinstance(variables, np.ndarray)
        assert isinstance(freq_refl, list)
        assert isinstance(fluxes_tran_empty, list)
        assert isinstance(fluxes_refl, list)
        assert isinstance(fluxes_tran, list)
        assert variables_original.shape[0] == variables.shape[0]
        assert len(freq_refl) == len(fluxes_tran_empty) == len(fluxes_refl) == len(fluxes_tran)

        freq_refl = np.array(freq_refl)
        fluxes_tran_empty = np.array(fluxes_tran_empty)
        fluxes_refl = np.array(fluxes_refl)
        fluxes_tran = np.array(fluxes_tran)

        assert len(freq_refl.shape) == len(fluxes_tran_empty.shape) == len(fluxes_refl.shape) == len(fluxes_tran.shape) == 1
        assert freq_refl.shape[0] == fluxes_tran_empty.shape[0] == fluxes_refl.shape[0] == fluxes_tran.shape[0]

        fluxes_refl *= -1.0
        wavelengths = 1 / freq_refl
        wavelengths *= self.unit_length
        num_wavelengths = wavelengths.shape[0]

        transmittance = np.zeros(num_wavelengths)
        reflectance = np.zeros(num_wavelengths)

        transmittance[fluxes_tran_empty > 0] = fluxes_tran[fluxes_tran_empty > 0] / fluxes_tran_empty[fluxes_tran_empty > 0]
        reflectance[fluxes_tran_empty > 0] = fluxes_refl[fluxes_tran_empty > 0] / fluxes_tran_empty[fluxes_tran_empty > 0]

        absorbance = 1.0 - transmittance - reflectance

        dict_all = {
            'name': self.name,
            'num_variables': self.num_variables,
            'unit_length': self.unit_length,
            'num_materials': self.num_materials,
            'variables_original': variables_original,
            'variables': variables,
            'materials': self.list_materials,
            'size_mesh': self.size_mesh,
            'resolution': self.resolution,
            'wavelengths': wavelengths,
            'transmittance': transmittance,
            'reflectance': reflectance,
            'absorbance': absorbance,
            'fluxes_tran_empty': fluxes_tran_empty,
            'fluxes_refl': fluxes_refl,
            'fluxes_tran': fluxes_tran,
        }

        print('', flush=True)
        self.print_separators()
        print(f'num_wavelengths {num_wavelengths}', flush=True)
        print(f'mean(wavelengths) {np.mean(wavelengths)}', flush=True)
        print(f'min(wavelengths) {np.min(wavelengths)}', flush=True)
        print(f'max(wavelengths) {np.max(wavelengths)}', flush=True)
        print(f'mean(fluxes_tran_emtpy) {np.mean(fluxes_tran_empty)}', flush=True)
        print(f'mean(fluxes_refl) {np.mean(fluxes_refl)}', flush=True)
        print(f'mean(fluxes_tran) {np.mean(fluxes_tran)}', flush=True)
        print('')

        print(f'mean(transmittance) {np.mean(transmittance)}', flush=True)
        print(f'mean(reflectance) {np.mean(reflectance)}', flush=True)
        print(f'mean(absorbance) {np.mean(absorbance)}', flush=True)
        self.print_separators()
        print('', flush=True)

        return dict_all

    def run_simulation_empty(self):
        if self.mode == 'decay':
            self.sim_empty.run(
                until_after_sources=mp.stop_when_fields_decayed(self.steps_for_decay, mp.Ez, self.point_to_measure, self.decay_by),
            )
        elif self.mode == 'fixed':
            self.sim_empty.run(until=2.0)
        else:
            raise ValueError

    def run_simulation(self):
        if self.mode == 'decay':
            if self.save_efields_hfields:
                path_intermediate = os.path.join(
                    self.path_outputs,
                    self.get_str_current_experiment()
                )

                if not os.path.exists(self.path_outputs):
                    os.mkdir(self.path_outputs)

                if not os.path.exists(path_intermediate):
                    os.mkdir(path_intermediate)

                self.sim.use_output_directory(os.path.join(
                    path_intermediate,
                    f'{self.prefix_file}'
                ))

                self.sim.run(
                    mp.at_beginning(mp.output_epsilon),
                    mp.to_appended("ez", mp.at_every(self.time_step, mp.output_efield_z)),
                    mp.to_appended("hz", mp.at_every(self.time_step, mp.output_hfield_z)),
                    until_after_sources=mp.stop_when_fields_decayed(
                        self.steps_for_decay, mp.Ez, self.point_to_measure, self.decay_by),
                )
            else:
                self.sim.run(
                    until_after_sources=mp.stop_when_fields_decayed(
                        self.steps_for_decay, mp.Ez, self.point_to_measure, self.decay_by),
                )
        elif self.mode == 'fixed':
            self.sim.run(until=2.0)
        else:
            raise ValueError

    def reset(self):
        self.sim_empty.reset_meep()
        self.sim.reset_meep()

    def get_limit_y(self):
        limit_y_positive = self.margin_structure * (0.5 * (self.size_cell[1] - 2 * self.depth_pml))
        limit_y_negative = self.margin_structure * (0.5 * (self.size_cell[1] - 2 * self.depth_pml) - self.depth_pml)

        return limit_y_positive, limit_y_negative

    def plot_2D(self, plot_sources=True, plot_monitors=True):
        if self.show_figures or self.save_figures:
            str_structure_empty, str_structure, str_efield_z, str_hfield_z = utils_io.get_str_figures(
                self.name)

            self.sim_empty.plot2D(
                plot_sources_flag=plot_sources,
                plot_monitors_flag=plot_monitors,
            )
            self.set_axis()
            if self.save_figures: plt.savefig(str_structure_empty)
            if self.show_figures: plt.show()

            self.sim.plot2D(
                plot_sources_flag=plot_sources,
                plot_monitors_flag=plot_monitors,
            )
            self.set_axis()
            if self.save_figures: plt.savefig(str_structure)
            if self.show_figures: plt.show()

            self.sim.plot2D(
                fields=mp.Ez,
                plot_sources_flag=plot_sources,
                plot_monitors_flag=plot_monitors,
            )
            self.set_axis()
            if self.save_figures: plt.savefig(str_efield_z)
            if self.show_figures: plt.show()

            self.sim.plot2D(
                fields=mp.Hz,
                plot_sources_flag=plot_sources,
                plot_monitors_flag=plot_monitors,
            )
            self.set_axis()
            if self.save_figures: plt.savefig(str_hfield_z)
            if self.show_figures: plt.show()

    def plot_3D(self, epsilons_empty, epsilons):
        if self.show_figures or self.save_figures:
            str_structure_empty, str_structure, str_efield_z, str_hfield_z = utils_io.get_str_figures(
                self.name)

            if self.show_figures: utils_io.visualize_3d(epsilons_empty)

            if self.show_figures: utils_io.visualize_3d(epsilons)

            if self.show_figures: utils_io.visualize_3d(epsilons)

            if self.show_figures: utils_io.visualize_3d(epsilons)

    def set_axis(self):
        ax = plt.gca()
        ax.invert_yaxis()

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        ax.set_xticks([])
        ax.set_yticks([])

        ax.xaxis.label.set_visible(False)
        ax.yaxis.label.set_visible(False)

    def get_str_current_experiment(self):
        str_current_experiment =  f'{self.name}_{"_".join(self.list_materials)}_{self.size_mesh}'
        return str_current_experiment

    def get_str_current_experiment_with_variables(self, variables):
        str_current_experiment =  f'{self.get_str_current_experiment()}_{"_".join(variables.astype(str))}'
        return str_current_experiment

    def get_path_current(self):
        path_current = os.path.join(
            self.path_properties,
            self.get_str_current_experiment()
        )

        return path_current

    def get_str_file(self, variables):
        str_current_experiment = self.get_str_current_experiment_with_variables(variables)
        str_file = f'{str_current_experiment}.npy'
        return str_file

    def save(self, dict_properties):
        if not os.path.exists(self.path_properties):
            os.mkdir(self.path_properties)

        path_current = self.get_path_current()
        str_file = self.get_str_file(dict_properties["variables"])

        if not os.path.exists(path_current):
            os.mkdir(path_current)

        path_file = os.path.join(path_current, str_file)
        print(f'saved at {path_file}')
        np.save(path_file, dict_properties)

    def print_experiment_info(self, variables):
        variables_parsed = self.parse(variables)

        print('', flush=True)
        self.print_separators()
        print(f'unit_length {self.unit_length}')
        print(f'size_mesh {self.size_mesh}')
        print(f'resolution {self.resolution}')
        print(f'size_cell_x {self.size_cell[0]} size_cell_y {self.size_cell[1]} size_cell_z {self.size_cell[2]}', flush=True)
        print('', flush=True)

        print(f'wavelength {self.wavelength}')
        print(f'depth_pml {self.depth_pml}')
        for label, variable in zip(self.labels, variables_parsed):
            print(f'{label} {variable}')
        self.print_separators()
        print('', flush=True)

    def transform(self, variable_or_variables):
        assert isinstance(variable_or_variables, (int, float, np.ndarray))

        if isinstance(variable_or_variables, float) and variable_or_variables == 1.1 and self.unit_length == 10:
            return 0.11

        return variable_or_variables / self.unit_length

    def _run(self, variables):
        time_start = time.time()
        variables_original = variables
        variables = self.transform(variables)

        self.change_size_cell(variables)
        self.print_experiment_info(variables)
        self.define_experiment(variables)

        self.run_simulation_empty()

        refl_empty_data = self.sim_empty.get_flux_data(self.refl_empty)
        fluxes_tran_empty = mp.get_fluxes(self.tran_empty)

        self.sim.load_minus_flux_data(self.refl, refl_empty_data)

        self.run_simulation()

        epsilons_empty = self.sim_empty.get_epsilon()
        epsilons = self.sim.get_epsilon()

        fluxes_refl = mp.get_fluxes(self.refl)
        fluxes_tran = mp.get_fluxes(self.tran)

        freq_refl = mp.get_flux_freqs(self.refl)
        assert np.all(np.array(freq_refl) == np.array(mp.get_flux_freqs(self.tran)))
        time_end = time.time()

        dict_all = self.compute_properties(
            variables_original,
            variables,
            freq_refl,
            fluxes_tran_empty,
            fluxes_refl,
            fluxes_tran
        )
        dict_all['time_elapsed'] = time_end - time_start

        if self.save_properties:
            self.save(dict_all)

        return dict_all, epsilons_empty, epsilons

    @property
    @abc.abstractmethod
    def num_variables(self):
        pass

    @property
    @abc.abstractmethod
    def num_materials(self):
        pass

    @property
    @abc.abstractmethod
    def labels(self):
        pass

    @abc.abstractmethod
    def verify_specific(self, variables):
        pass

    @abc.abstractmethod
    def define_geometries(self):
        pass

    @abc.abstractmethod
    def parse(self, variables):
        pass

    @abc.abstractmethod
    def change_size_cell(self, variables):
        pass

    @abc.abstractmethod
    def run(self, variables):
        pass

    def __call__(self, variables):
        self.run(variables)
