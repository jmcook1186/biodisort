import codecs
import os

from setuptools import find_packages, setup


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")


setup(
    name="biodisort",
    package_dir={"": "biodisort"},
    packages=find_packages(where="biodisort"),
    version=get_version("biodisort/__init__.py"),
    author="Joseph Cook",
    author_email="biosnicar@proton.me",
    description="Snow and ice albedo modelling in Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "Bug Tracker": "https://github.com/jmcook1186/biodisort-py/issues",
        "Source": "https://github.com/jmcook1186/biodisort-py",
        "Documentation": "",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Hydrology",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "dask",
        "click==8",
        "matplotlib",
        "miepython",
        "pandas",
        "scipy",
        "seaborn",
        "xarray",
        "plotnine",
        "statsmodels",
        "pydisort",
        "netcdf4",
    ],
)
