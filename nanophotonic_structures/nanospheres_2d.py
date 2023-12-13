import numpy as np
import meep as mp

from nanophotonic_structures import base_structure
from nanophotonic_structures import constants


class Nanospheres2D(base_structure.BaseStructure):
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
        wavelength = constants.wavelength_solar

        super().__init__(
            name, mode, size_cell, depth_pml, size_mesh, materials,
            show_figures, save_figures, save_properties, save_efields_hfields, wavelength
        )

    @property
    def num_variables(self):
        return 2

    @property
    def num_materials(self):
        return 2

    @property
    def labels(self):
        return ['thickness', 'radius']

    def verify_specific(self, variables):
        assert variables.shape[0] == self.num_variables
        assert len(self.list_materials) == self.num_materials

        thickness, radius = self.parse(variables)
        limit_y_positive, limit_y_negative = self.get_limit_y()

        assert 2 * radius <= limit_y_negative
        assert thickness <= limit_y_positive

        assert self.size_cell[2] == 0

    def define_geometries(self, variables):
        thickness, radius = self.parse(variables)

        material_plate = self.materials[0]
        material_spheres = self.materials[1]

        self.geometries = [
            mp.Block(
                size=mp.Vector3(mp.inf, thickness, mp.inf),
                center=mp.Vector3(0, 0.5 * thickness, 0),
                material=material_plate,
            ),

            mp.Cylinder(
                radius=radius,
                height=mp.inf,
                center=mp.Vector3(0, -radius, 0),
                axis=mp.Vector3(0, 0, 1),
                material=material_spheres,
            ),
        ]

    def parse(self, variables):
        thickness = variables[0]
        radius = variables[1]

        return thickness, radius

    def change_size_cell(self, variables):
        thickness, radius = self.parse(variables)

        if not self.use_fixed_size_cell:
            self.size_cell = [
                2 * radius,
                2 * np.maximum(thickness, 2 * radius) + 4 * self.depth_pml + 2 * self.depth_pml,
                0
            ]
        else:
            self.size_cell = [
                2 * radius,
                self.size_cell[1],
                self.size_cell[2]
            ]

    def run(self, variables):
        dict_all, _, _ = self._run(variables)

        self.plot_2D()
        self.reset()

        return dict_all


if __name__ == '__main__':
    obj = Nanospheres2D(
        depth_pml=50,
        size_mesh=10,
        mode='fixed',
        materials=['test_1.8', 'test_2.4'],
        show_figures=False,
        save_figures=False,
        save_efields_hfields=False,
    )

    variables = np.array([60, 30])

    obj.run(variables)
