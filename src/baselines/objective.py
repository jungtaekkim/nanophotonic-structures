import numpy as np


class Objective:
    def __init__(self, fun_target, bounds):
        self.function = fun_target
        self.bounds = bounds
        self.X = []
        self.Y = []

        bounds_filtered = []

        for bound in bounds:
            if bound[0] < bound[1]:
                bounds_filtered.append(bound)
        bounds_filtered = np.array(bounds_filtered)

        self.bounds_filtered = bounds_filtered
        self.bounds_filtered_tuple = (bounds_filtered[:, 0], bounds_filtered[:, 1])

    def filter(self, bx):
        return bx[self.bounds[:, 0] < self.bounds[:, 1]]

    def recover(self, bx):
        bx_to_evaluate = np.zeros(self.bounds.shape[0])

        bx_to_evaluate[self.bounds[:, 0] < self.bounds[:, 1]] = bx
        bx_to_evaluate[self.bounds[:, 0] == self.bounds[:, 1]] = self.bounds[self.bounds[:, 0] == self.bounds[:, 1], 0]

        return bx_to_evaluate

    def __call__(self, bx):
        bx_to_evaluate = self.recover(bx)
        y = self.function(bx_to_evaluate)

        self.X.append(bx_to_evaluate)
        self.Y.append([y])

        return y
