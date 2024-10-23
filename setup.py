#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name="pyuff_ustb",
    version="3.0.0",
    author_email="magnus.kvalevag@ntnu.no",
    packages=find_packages(),
    install_requires=["numpy", "h5py"],
)
