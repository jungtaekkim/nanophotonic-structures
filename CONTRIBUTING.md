# Contributing to "Datasets and Benchmarks for Nanophotonic Structure and Parametric Design Simulations"

Thanks for taking the time to contribute to the project.

The following is a set of guidelines for contributing to "Datasets and Benchmarks for Nanophotonic Structure and Parametric Design Simulations".

## Code of Conduct

This project and everyone participating in it is governed by the [Code of Conduct](CODE_OF_CONDUCT.md). Please report unacceptable behavior if you face it.

## How Can I Contribute?

This section describes how you can contribute to the project. You can suggest your contributions via two ways: reporting issues and submitting pull requests.

### Reporting Bugs

To report bugs, you can use an issue template on a bug report.  Please follow the description in the template.

### Requesting Features

You can use an issue template on a feature request.  Please follow the description in the template.

### Suggesting New Nanophotonic Structures

If you want to suggest a new nanophotonic structure, you can use an issue template on a new structure suggestion.

Please see the [abstract class](nanophotonic_structures/base_structure.py) for understanding what you should specify.

For your information, part of the abstract class is described here.

```python
class BaseStructure(abc.ABC):
    def __init__(
        self,
        name, # an experiment name
        mode, # a simulation mode, decay or fixed
        size_cell, # the size of a simulation cell
        depth_pml, # the depth of a PML layer
        resolution, # resolution
        materials, # list of materials
        show_figures, # a flag for showing figures
        save_figures, # a flag for saving figures
        save_properties, # a flag for saving properties
        save_efields_hfields, # a flag for saving E-fields and H-fields
        wavelength, # a wavelength, a sinlge value of a tuple of min and max wavelengths
        eps_averaging=False, # a flag for eps_averaging
        time_step=2.0, # a time step
        path_outputs='../../outputs-nanophotonic-structures', # a path to save outputs
        path_properties='../../datasets-nanophotonic-structures', # a path to save properties
    ):
```

In particular, please include the references on the new structures.

### Pull Requests

You can freely submit a pull request to contribute to this project.

If you want to add new nanophotonic structures, please declare the following properties defined in the [BaseStructure class](nanophotonic_structures/base_structure.py) appropriately.

```python
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
```

`num_variables` indicates the number of variables. For example, it is 3 if three parameters are involved in a structure.

`num_materials` stands for the number of materials. It can be different from `num_variables`.

`labels` is to define the names of variables. For example, if two variables are related to pitch and radius respectively, it is ['pitch', 'radius'].

`verify_specific` is to verify constraints for the structure of interest.

`define_geometries` is to model the structure using the geometries defined in [Meep](https://github.com/NanoComp/meep); please see its documentation.

`parse` is used to parse variables by taking a vector. For example, supposing that `labels` is ['pitch', 'radius'], pitch is x1 and radius is x2 if [x1, x2] is provided.

`change_size_cell` is to change the size of a simulation cell.

`run` is a function to run a simulation.

If you are not familiar with these properties, please refer to [one example](nanophotonic_structures/threelayers_2d.py) of the structures implemented in the project.
