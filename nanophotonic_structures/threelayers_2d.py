import numpy as np
import meep as mp

from nanophotonic_structures import base_structure
from nanophotonic_structures import constants


class ThreeLayers2D(base_structure.BaseStructure):
    def __init__(
        self,
        depth_pml,
        size_mesh,
        materials,
        size_cell=None,
        mode='decay',
        show_figures=False,
        save_figures=False,
        save_properties=False,
        save_efields_hfields=False,
    ):
        name = self.__class__.__name__.lower()
        wavelength = constants.wavelength_default

        super().__init__(
            name, mode, size_cell, depth_pml, size_mesh, materials,
            show_figures, save_figures, save_properties, save_efields_hfields, wavelength
        )

    @property
    def num_variables(self):
        return 3

    @property
    def num_materials(self):
        return 3

    @property
    def labels(self):
        return ['thickness_first', 'thickness_second', 'thickness_third']

    def verify_specific(self, variables):
        assert variables.shape[0] == self.num_variables
        assert len(self.list_materials) == self.num_materials

        thickness_first, thickness_second, thickness_third = self.parse(variables)
        limit_y_positive, limit_y_negative = self.get_limit_y()

        assert (thickness_first + 0.5 * thickness_second) <= limit_y_negative
        assert (thickness_third + 0.5 * thickness_second) <= limit_y_positive

        assert self.size_cell[2] == 0

    def define_geometries(self, variables):
        thickness_first, thickness_second, thickness_third = self.parse(variables)

        material_first = self.materials[0]
        material_second = self.materials[1]
        material_third = self.materials[2]

        self.geometries = [
            mp.Block(
                size=mp.Vector3(mp.inf, thickness_first, mp.inf),
                center=mp.Vector3(0, -1.0 * (thickness_first + thickness_second) / 2.0, 0),
                material=material_first,
            ),
            mp.Block(
                size=mp.Vector3(mp.inf, thickness_second, mp.inf),
                center=mp.Vector3(0, 0, 0),
                material=material_second,
            ),
            mp.Block(
                size=mp.Vector3(mp.inf, thickness_third, mp.inf),
                center=mp.Vector3(0, (thickness_third + thickness_second) / 2.0, 0),
                material=material_third,
            ),
        ]

    def parse(self, variables):
        thickness_first = variables[0]
        thickness_second = variables[1]
        thickness_third = variables[2]

        return thickness_first, thickness_second, thickness_third

    def change_size_cell(self, variables):
        thickness_first, thickness_second, thickness_third = self.parse(variables)

        if not self.use_fixed_size_cell:
            self.size_cell = [
                self.transform(10),
                thickness_second + 2 * np.maximum(thickness_first, thickness_third) + 4 * self.depth_pml + 2 * self.depth_pml,
                0
            ]

    def run(self, variables):
        dict_all, _, _ = self._run(variables)

        self.plot_2D()
        self.reset()

        return dict_all


if __name__ == '__main__':
    obj = ThreeLayers2D(
        depth_pml=50,
        size_mesh=10,
        mode='fixed',
        materials=['test_1.8', 'test_2.4', 'test_1.8'],
        show_figures=False,
        save_figures=False,
        save_efields_hfields=False,
    )

    variables = np.array([35, 20, 50])

    obj.run(variables)
