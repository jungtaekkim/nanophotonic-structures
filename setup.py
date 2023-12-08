from setuptools import setup


path_requirements = 'requirements.txt'
list_packages = ['nanophotonic_structures']

with open(path_requirements) as f:
    required = f.read().splitlines()

setup(
    name='nanophotonic-structures',
    version='0.1.0',
    author='Jungtaek Kim',
    author_email='jungtaek.kim.mail@gmail.com',
    url='https://github.com/jungtaekkim/nanophotonic-structures',
    license='MIT',
    description='Datasets and Benchmarks for Nanophotonic Structure and Parametric Design Simulations',
    packages=list_packages,
    python_requires='>=3.7, <4',
    install_requires=required,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ]
)
