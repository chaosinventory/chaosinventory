#!/usr/bin/bash


git_dir=$(git rev-parse --show-toplevel)
cd "${git_dir}/scripts/" || exit

./lint.py
exit $?
