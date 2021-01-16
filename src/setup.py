from pathlib import Path
from setuptools import find_packages, setup

here = Path(__file__).resolve().parent

with open(here.parent / 'README.md') as readme:
    long_description = readme.read()

setup(
    long_description=long_description,
)
