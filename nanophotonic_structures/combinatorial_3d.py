import numpy as np
import meep as mp

from nanophotonic_structures import base_structure
from nanophotonic_structures import constants


class Combinatorial3D(base_structure.BaseStructure):
    def __init__(
        self,
        depth_pml,
        size_mesh,
        size_cell=None,
        mode='decay',
        show_figures=False,
        save_figures=False,
        save_properties=False,
        save_efields_hfields=False,
    ):
        name = self.__class__.__name__.lower()
        wavelength = constants.wavelength_solar
        materials = [
            'Ag', 'air', 'Au', 'AZO', 'cSi', 'CH3NH3PbI3',
            'Cu', 'GaAs', 'ITO', 'Ni', 'TiO2', 'ZnO',
        ]

        super().__init__(
            name, mode, size_cell, depth_pml, size_mesh, materials,
            show_figures, save_figures, save_properties, save_efields_hfields, wavelength
        )

        self.index_air = 1
        self.size_material_block = self.transform(10)
        self.size_repeating_unit_x = self.transform(200)
        self.size_repeating_unit_y = self.transform(200)
        self.size_repeating_unit_z = self.transform(40)

        self.num_x = int(self.size_repeating_unit_x // self.size_material_block)
        self.num_y = int(self.size_repeating_unit_y // self.size_material_block)
        self.num_z = int(self.size_repeating_unit_z // self.size_material_block)

    @property
    def num_variables(self):
        return self.num_x * self.num_y * self.num_z

    @property
    def num_materials(self):
        return 12

    @property
    def labels(self):
        return [f'material_block_{index:04d}' for index in range(0, self.num_variables)]

    def verify_specific(self, variables):
        assert variables.shape[0] == self.num_variables
        assert len(self.list_materials) == self.num_materials

        variables_recovered = variables * self.unit_length
        variables_recovered = variables_recovered.astype(np.int64)

        assert np.all(0 <= variables_recovered)
        assert np.all(variables_recovered < self.num_materials)

        limit_y_positive, limit_y_negative = self.get_limit_y()

        assert self.size_repeating_unit_z * 0.5 <= limit_y_negative
        assert self.size_repeating_unit_z * 0.5 <= limit_y_positive

        assert self.size_material_block == self.transform(10)
        assert self.size_repeating_unit_x == self.transform(200)
        assert self.size_repeating_unit_y == self.transform(200)
        assert self.size_repeating_unit_z == self.transform(40)

        assert self.num_x == 20
        assert self.num_y == 20
        assert self.num_z == 4

        assert self.list_materials[self.index_air] == 'air'

    def define_geometries(self, variables):
        variables_recovered = variables * self.unit_length
        variables_recovered = variables_recovered.astype(np.int64)

        geometries = []

        for ind_block_x in range(0, self.num_x):
            for ind_block_y in range(0, self.num_y):
                for ind_block_z in range(0, self.num_z):
                    current_index = ind_block_x * self.num_y * self.num_z + ind_block_y * self.num_z + ind_block_z
                    center_x = ind_block_x * self.size_material_block - self.size_repeating_unit_x / 2 + self.size_material_block / 2
                    center_y = ind_block_y * self.size_material_block - self.size_repeating_unit_y / 2 + self.size_material_block / 2
                    center_z = ind_block_z * self.size_material_block - self.size_repeating_unit_z / 2 + self.size_material_block / 2

                    if variables_recovered[current_index] == self.index_air:
                        continue

                    material_block = mp.Block(
                        size=mp.Vector3(self.size_material_block, self.size_material_block, self.size_material_block),
                        center=mp.Vector3(center_x, center_z, center_y),
                        material=self.materials[variables_recovered[current_index]],
                    )

                    geometries.append(material_block)

        self.geometries = geometries

    def parse(self, variables):
        # not used for this structure
        return variables

    def change_size_cell(self, variables):
        if not self.use_fixed_size_cell:
            self.size_cell = [
                self.size_repeating_unit_x,
                self.size_repeating_unit_z + 4 * self.depth_pml + 2 * self.depth_pml,
                self.size_repeating_unit_y,
            ]
        else:
            self.size_cell = [
                self.size_repeating_unit_x,
                self.size_cell[1],
                self.size_repeating_unit_y,
            ]

    def run(self, variables):
        dict_all, epsilons_empty, epsilons = self._run(variables)

        self.plot_3D(epsilons_empty, epsilons)
        self.reset()

        return dict_all


if __name__ == '__main__':
    obj = Combinatorial3D(
        depth_pml=50,
        size_mesh=10,
        mode='fixed',
        show_figures=False,
        save_figures=False,
        save_efields_hfields=False,
    )

    variables = np.random.RandomState(42).choice(12, size=1600)

    obj.run(variables)
