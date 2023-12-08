import numpy as np
import meep as mp

from nanophotonic_structures import base_structure
from nanophotonic_structures import constants


class DoubleNanocones3D(base_structure.BaseStructure):
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
        wavelength = constants.wavelength_visible

        super().__init__(
            name, mode, size_cell, depth_pml, size_mesh, materials,
            show_figures, save_figures, save_properties, save_efields_hfields, wavelength
        )

    @property
    def num_variables(self):
        return 7

    @property
    def num_materials(self):
        return 5

    @property
    def labels(self):
        return [
            'thickness_first', 'thickness_second', 'thickness_third',
            'radius_first', 'height_first',
            'radius_second', 'height_second'
        ]

    def verify_specific(self, variables):
        assert variables.shape[0] == self.num_variables
        assert len(self.list_materials) == self.num_materials

        thickness_first, thickness_second, thickness_third, radius_first, height_first, radius_second, height_second = self.parse(variables)
        limit_y_positive, limit_y_negative = self.get_limit_y()

        assert (thickness_first + 0.5 * thickness_second + height_first) <= limit_y_negative
        assert (thickness_third + 0.5 * thickness_second + height_second) <= limit_y_positive

    def define_geometries(self, variables):
        thickness_first, thickness_second, thickness_third, radius_first, height_first, radius_second, height_second = self.parse(variables)

        material_first = self.materials[0]
        material_second = self.materials[1]
        material_third = self.materials[2]
        material_cones_first = self.materials[3]
        material_cones_second = self.materials[4]

        offset_first = -0.5 * thickness_second - thickness_first
        offset_second = 0.5 * thickness_second + thickness_third

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

            mp.Cone(
                radius=0,
                radius2=radius_first,
                height=height_first,
                center=mp.Vector3(0, offset_first - height_first / 2, 0),
                axis=mp.Vector3(0, 1, 0),
                material=material_cones_first,
            ),
            mp.Cone(
                radius=radius_first,
                radius2=0,
                height=height_second,
                center=mp.Vector3(0, offset_second + height_first / 2, 0),
                axis=mp.Vector3(0, 1, 0),
                material=material_cones_second,
            ),
        ]

    def parse(self, variables):
        thickness_first = variables[0]
        thickness_second = variables[1]
        thickness_third = variables[2]

        radius_first = variables[3]
        height_first = variables[4]

        radius_second = variables[5]
        height_second = variables[6]

        return thickness_first, thickness_second, thickness_third, radius_first, height_first, radius_second, height_second

    def change_size_cell(self, variables):
        thickness_first, thickness_second, thickness_third, radius_first, height_first, radius_second, height_second = self.parse(variables)

        if not self.use_fixed_size_cell:
            self.size_cell = [
                2 * np.maximum(radius_first, radius_second),
                thickness_second + 2 * np.maximum(thickness_first, thickness_third) + 2 * np.maximum(height_first, height_second) + 4 * self.depth_pml + 2 * self.depth_pml,
                2 * np.maximum(radius_first, radius_second),
            ]
        else:
            self.size_cell = [
                2 * np.maximum(radius_first, radius_second),
                self.size_cell[1],
                2 * np.maximum(radius_first, radius_second),
            ]

    def run(self, variables):
        dict_all, epsilons_empty, epsilons = self._run(variables)

        self.plot_3D(epsilons_empty, epsilons)
        self.reset()

        return dict_all


if __name__ == '__main__':
    obj = DoubleNanocones3D(
        depth_pml=50,
        size_mesh=10,
        mode='fixed',
        materials=['test_2.4', 'test_1.8', 'test_2.4', 'test_6.25', 'test_6.25'],
        show_figures=False,
        save_figures=False,
        save_efields_hfields=False,
    )

    variables = np.array([30, 25, 40, 30, 20, 15, 30])

    obj.run(variables)
