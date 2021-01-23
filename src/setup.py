from pathlib import Path

from setuptools import setup

here = Path(__file__).resolve().parent

with open(here.parent / 'README.md') as readme:
    long_description = readme.read()

setup(
    long_description=long_description,
)
