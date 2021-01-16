from pathlib import Path

from setuptools import find_packages, setup

import chaosinventory

here = Path(__file__).resolve().parent

with open(here.parent / 'README.md') as readme:
    long_description = readme.read()

setup(
    name='chaosinventory',
    version=chaosinventory.__version__,
    python_requires='>=3.5',
    description = '',
    long_description=long_description,
    url='https://github.com/chaosinventory/',
    author='Chaosinventory Team',
    license='AGPL-3.0',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
    keywords ='chaos inventory organisation blåhaj',
    install_requires=[
        'Django==3.1.*',
        'psycopg2-binary'
    ],
    packages=find_packages(),
    entry_points = {
        'console_scripts': [
            'chaosinventory = chaosinventory.__main__:main'
        ]
    }
)
