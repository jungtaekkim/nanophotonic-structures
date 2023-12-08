import numpy as np
import meep as mp

from nanophotonic_structures import base_structure
from nanophotonic_structures import constants


class Nanocones2D(base_structure.BaseStructure):
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
        return ['radius', 'height']

    def verify_specific(self, variables):
        assert variables.shape[0] == self.num_variables
        assert len(self.list_materials) == self.num_materials

        radius, height = self.parse(variables)
        limit_y_positive, limit_y_negative = self.get_limit_y()

        assert height <= limit_y_negative

        assert self.size_cell[2] == 0

    def define_geometries(self, variables):
        radius, height = self.parse(variables)

        material_plate = self.materials[0]
        material_cones = self.materials[1]

        height_plate = height + 2 * self.depth_pml + 0.9 * self.depth_pml

        self.geometries = [
            mp.Block(
                size=mp.Vector3(mp.inf, height_plate, mp.inf),
                center=mp.Vector3(0, 0.5 * height_plate, 0),
                material=material_plate,
            ),

            mp.Prism(
                vertices=[
                    mp.Vector3(0, -height, 0),
                    mp.Vector3(-radius, 0, 0),
                    mp.Vector3(radius, 0, 0),
                ],
                height=mp.inf,
                axis=mp.Vector3(0, 0, 1),
                material=material_cones,
            ),
        ]

    def parse(self, variables):
        radius = variables[0]
        height = variables[1]

        return radius, height

    def change_size_cell(self, variables):
        radius, height = self.parse(variables)

        if not self.use_fixed_size_cell:
            self.size_cell = [
                2 * radius,
                2 * height + 4 * self.depth_pml + 2 * self.depth_pml,
                0
            ]
        else:
            self.size_cell = [
                2 * radius,
                self.size_cell[1],
                self.size_cell[2],
            ]

    def run(self, variables):
        dict_all, _, _ = self._run(variables)

        self.plot_2D()
        self.reset()

        return dict_all


if __name__ == '__main__':
    obj = Nanocones2D(
        depth_pml=50,
        size_mesh=10,
        mode='fixed',
        materials=['test_1.8', 'test_2.4'],
        show_figures=False,
        save_figures=False,
        save_efields_hfields=False,
    )

    variables = np.array([30, 60])

    obj.run(variables)
