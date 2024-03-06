# Datasets and Benchmarks for Nanophotonic Structure and Parametric Design Simulations

It is an official repository of the paper entitled "Datasets and Benchmarks for Nanophotonic Structure and Parametric Design Simulations", which is presented at NeurIPS 2023 Datasets and Benchmarks track.

* [Project page](https://jungtaekkim.github.io/nanophotonic-structures)
* [arXiv preprint](https://arxiv.org/abs/2310.19053)
* [NeurIPS proceedings](https://proceedings.neurips.cc)
* [GitHub repository](https://github.com/jungtaekkim/nanophotonic-structures)
* [Hugging Face repository](https://huggingface.co/datasets/jungtaekkim/datasets-nanophotonic-structures)

## Directories

* nanophotonic_structures: a directory for nanophotonic structures and utils
* scripts: a directory for runnable scripts
* src: a directory for dataset generation, model training, model testing, and structure optimization

## Scripts

* generate_datset.sh: a script for dataset generation
* optimize_models_continuous.sh: a script for nanophotonic structure optimization over continuous spaces
* optimize_models_discrete.sh: a script for nanophotonic structure optimization over discrete spaces
* train_models.sh: a script for surrogate model training
* test_models.sh: a script for surrogate model testing

## Installation

Before installing our package, you should install `meep` first.  A guide to the installation of `meep` is provided in [this link](https://github.com/NanoComp/meep).

Our package can be installed from source or from source in an editable mode.

```console
pip install .
```
or
```console
pip install -r requirements.txt
python setup.py develop
```

## Access to Datasets

If you want to create datasets by yourself, you can use scripts in the `scripts` directory.

Our datasets can be accessed via [the Hugging Face repository](https://huggingface.co/datasets/jungtaekkim/datasets-nanophotonic-structures).


## Citation

```
@inproceedings{KimJ2023neuripsdb,
    author={Kim, Jungtaek and Li, Mingxuan and Hinder, Oliver and Leu, Paul W.},
    title={Datasets and Benchmarks for Nanophotonic Structure and Parametric Design Simulations},
    booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
    volume={36},
    pages={4685--4715},
    year={2023},
    note={Datasets and Benchmarks Track}
}
```

## Instructions to Contribute to the Project

We are open to any users who want to contribute to the project.
You can refer to [instructions](CONTRIBUTING.md) to know how you can contribute to the project.

## License

It is licensed under the [MIT license](LICENSE).

## Code of Conduct

We follow the [code of conduct](CODE_OF_CONDUCT.md) to create a diverse, inclusive, and postive community.
