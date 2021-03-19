#!/usr/bin/env python3

"""
Linting script for the chaosinventory core to be invoked manually
or using a git pre-commit hook.

.. todo:: Let the script check itself

.. todo::

    Update this to work in a functional manner so that the checks are
    only executed when the script is called directly
    :code:`(__name__ == '__main')` and thus autodoc can be used on it
    and checking of more folders can be added easier.
"""

import argparse
import os
import subprocess
from pathlib import Path


# Sourced from the blender build scripts via
# https://stackoverflow.com/a/287944/11249686
# We can not import this from a separate file since it would not be
# present if executed as a git hook
class Colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def passed_failed(b, color=None, prefix=None, highlight=False):
    if color is None:
        color = not args.no_color

    if not color:
        return 'passed' if b else 'failed'

    response = ''

    if highlight:
        response += Colors.UNDERLINE
        response += Colors.BOLD

    if prefix:
        # If we would just append str(None) we would get a litteral
        # "None" in the output
        response += prefix

    response += Colors.OKGREEN if b else Colors.FAIL
    response += 'passed' if b else 'failed'
    response += Colors.ENDC

    return response


parser = argparse.ArgumentParser(description=(
    'Linting script for the chaosinventory core to be invoked manually'
    'or using a git pre-commit hook.'
))

parser.add_argument(
    '--fix',
    action='store_true',
    help='Fix issues if possible',
)
parser.add_argument(
    '--no-color',
    action='store_true',
    help='Display colorfull summary',
)
args = parser.parse_args()

# Path detection
# By default we will try to get it from git
git_dir_proc = subprocess.run(
    [
        'git',
        'rev-parse',
        '--show-toplevel'
    ],
    capture_output=True
)
git_dir = git_dir_proc.stdout

# and fall back to mapping it relatively from our own location
if git_dir_proc.stdout and not git_dir_proc.returncode:
    git_dir = git_dir.decode('utf-8').strip()
    basepath = Path(git_dir).absolute()
else:
    basepath = Path(__file__).absolute().parents[1]

basepath /= 'src'
print('Testing the code under {}'.format(basepath))
print('\nRunning isort...')

# Run as subprocess for maximum compatibility
isort_subprocess_args = [
    'isort',
    '--color',
    '-q',
    '.'
]

if not args.fix:
    isort_subprocess_args.append('--check')

isort_exit = subprocess.run(
    isort_subprocess_args,
    env=os.environ.copy(),
    cwd=basepath,
)
isort_passed = not isort_exit.returncode
print(passed_failed(isort_passed))

print('\nRunning flake8...')
flake8_subprocess_args = ['flake8', '.', '--show-source']
flake8_exit = subprocess.run(
    flake8_subprocess_args,
    env=os.environ.copy(),
    cwd=basepath
)
flake8_passed = not flake8_exit.returncode
print(passed_failed(flake8_passed))

all_passed = isort_passed and flake8_passed

print(passed_failed(
    all_passed,
    prefix='\nSummary:\t',
    highlight=True,
))
print('isort:\t\t{}'.format(passed_failed(isort_passed)))
print('flake8:\t\t{}'.format(passed_failed(flake8_passed)))

exit(not(all_passed))
