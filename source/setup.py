from setuptools import setup
from setuptools import find_packages
from mach8 import version

setup(
    name = 'mach8',
    version = version.string(), 
    packages = find_packages(),
)
