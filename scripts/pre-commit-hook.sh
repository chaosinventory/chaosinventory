#!/usr/bin/bash


git_dir=$(git rev-parse --show-toplevel)
cd "${git_dir}/scripts/" || exit

./lint.py
lint_exit=$?

cd "${git_dir}/src/" || exit
./manage.py test tests
test_exit=$?

if [ $lint_exit -ne 0 ]; then
  exit $lint_exit
fi

if [ $test_exit -ne 0 ]; then
  exit $test_exit
fi

exit 0
