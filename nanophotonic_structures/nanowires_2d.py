import numpy as np
import meep as mp

from nanophotonic_structures import base_structure
from nanophotonic_structures import constants


class Nanowires2D(base_structure.BaseStructure):
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
        return 3

    @property
    def num_materials(self):
        return 1

    @property
    def labels(self):
        return ['pitch_m_two_radius', 'radius', 'height']

    def verify_specific(self, variables):
        assert variables.shape[0] == self.num_variables
        assert len(self.list_materials) == self.num_materials

        pitch_m_two_radius, radius, height = self.parse(variables)
        limit_y_positive, limit_y_negative = self.get_limit_y()

        assert 0.5 * height <= limit_y_negative
        assert 0.5 * height <= limit_y_positive

        assert self.size_cell[2] == 0

    def define_geometries(self, variables):
        pitch_m_two_radius, radius, height = self.parse(variables)

        material = self.materials[0]

        self.geometries = [
            mp.Block(
                size=mp.Vector3(2 * radius, height, mp.inf),
                center=mp.Vector3(0, 0, 0),
                material=material,
            ),
        ]

    def parse(self, variables):
        pitch_m_two_radius = variables[0]
        radius = variables[1]
        height = variables[2]

        return pitch_m_two_radius, radius, height

    def change_size_cell(self, variables):
        pitch_m_two_radius, radius, height = self.parse(variables)

        if not self.use_fixed_size_cell:
            self.size_cell = [
                pitch_m_two_radius + 2 * radius,
                height + 4 * self.depth_pml + 2 * self.depth_pml,
                0
            ]
        else:
            self.size_cell = [
                pitch_m_two_radius + 2 * radius,
                self.size_cell[1],
                self.size_cell[2]
            ]

    def run(self, variables):
        dict_all, _, _ = self._run(variables)

        self.plot_2D()
        self.reset()

        return dict_all


if __name__ == '__main__':
    obj = Nanowires2D(
        depth_pml=50,
        size_mesh=10,
        mode='fixed',
        materials=['test_1.8'],
        show_figures=False,
        save_figures=False,
        save_efields_hfields=False,
    )

    variables = np.array([10, 20, 120])

    obj.run(variables)
