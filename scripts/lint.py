#!/usr/bin/env python3

import argparse
import os
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser(description='Check chaosinventory codestyle')
parser.add_argument('--fix', action="store_true",
                    help='Fix issues if possible')

args = parser.parse_args()

basepath = Path(__file__).absolute().parents[1]

print("Testing the code under %s" % basepath)

all_succeeded = True

# Analysis 1: isort
# Run as subprocess for maximum compatibility

print("Running isort")

isort_subprocess_args = ["isort", "--color", "-q", "."]
if not args.fix:
    isort_subprocess_args.append("--check")

isort_exit = subprocess.run(isort_subprocess_args,
                            env=os.environ.copy(), cwd=basepath / "src")

isort_passed = True

if isort_exit.returncode != 0:
    isort_passed = False
    all_succeeded = False

# Analysis 2: flake8

print("Running flake8")

flake8_subprocess_args = ["flake8", ".", "--show-source"]

flake8_exit = subprocess.run(flake8_subprocess_args,
                             env=os.environ.copy(), cwd=basepath / "src")

flake8_passed = True

if flake8_exit.returncode != 0:
    flake8_passed = False
    all_succeeded = False

# TODO: We have not tested the scripts itself yet.

# Finalize tests and output results


def passedFailed(b):

    if b:
        return "passed"
    else:
        return "failed"


print("Summary: %s" % passedFailed(all_succeeded))
print("isort: %s" % passedFailed(isort_passed))
print("flake8: %s" % passedFailed(flake8_passed))
