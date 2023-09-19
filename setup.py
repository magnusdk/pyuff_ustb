#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="pyuff_ustb",
    version="2.0.4",
    author_email="magnus.kvalevag@ntnu.no",
    packages=find_packages(),
    install_requires=["numpy", "h5py"],
)
