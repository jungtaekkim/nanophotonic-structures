import numpy as np
import meep as mp

from nanophotonic_structures import base_structure
from nanophotonic_structures import constants


class NotPackedNanocones3D(base_structure.BaseStructure):
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
        return 2

    @property
    def labels(self):
        return ['radius', 'height', 'pitch']

    def verify_specific(self, variables):
        assert variables.shape[0] == self.num_variables
        assert len(self.list_materials) == self.num_materials

        radius, height, pitch = self.parse(variables)
        limit_y_positive, limit_y_negative = self.get_limit_y()

        assert height <= limit_y_negative
        assert 2 * radius <= pitch

    def define_geometries(self, variables):
        radius, height, pitch = self.parse(variables)

        material_plate = self.materials[0]
        material_cones = self.materials[1]

        height_plate = height + 2 * self.depth_pml + 0.9 * self.depth_pml

        self.geometries = [
            mp.Block(
                size=mp.Vector3(mp.inf, height_plate, mp.inf),
                center=mp.Vector3(0, 0.5 * height_plate, 0),
                material=material_plate,
            ),

            mp.Cone(
                radius=0,
                radius2=radius,
                height=height,
                center=mp.Vector3(0, -height / 2, 0),
                axis=mp.Vector3(0, 1, 0),
                material=material_cones,
            ),
        ]

    def parse(self, variables):
        radius = variables[0]
        height = variables[1]
        pitch = variables[2]

        return radius, height, pitch

    def change_size_cell(self, variables):
        radius, height, pitch = self.parse(variables)

        if not self.use_fixed_size_cell:
            self.size_cell = [
                pitch,
                2 * height + 4 * self.depth_pml + 2 * self.depth_pml,
                pitch,
            ]
        else:
            self.size_cell = [
                pitch,
                self.size_cell[1],
                pitch,
            ]

    def run(self, variables):
        dict_all, epsilons_empty, epsilons = self._run(variables)

        self.plot_3D(epsilons_empty, epsilons)
        self.reset()

        return dict_all


if __name__ == '__main__':
    obj = NotPackedNanocones3D(
        depth_pml=50,
        size_mesh=10,
        mode='fixed',
        materials=['test_1.8', 'test_2.4'],
        show_figures=False,
        save_figures=False,
        save_efields_hfields=False,
    )

    variables = np.array([25, 30, 80])

    obj.run(variables)
