#!/bin/bash

# If this script would be run from a hook, we would not need to do this.
# But however, since this can also be run interactively, we need to
# make sure that we are in the appropriate location. This is done by
# getting the location of our git working directory and navigating to
# the src folder, also the location of the flake8 and isort
# configuration within the setup.ini
git_dir=$(git rev-parse --show-toplevel)
cd "${git_dir}/src/" || exit

isort --color --check . -q
isortExit=$?

flake8 . --show-source
flakeExit=$?

printf "isort:\t"

if [[ $isortExit -eq 0 ]]
then
  echo -e "\033[0;32mpass\033[0m"
else
  echo -e "\033[0;31mfailed\033[0m"
fi

printf "flake8:\t"

if [[ $flakeExit -eq 0 ]]
then
  echo -e "\033[0;32mpass\033[0m"
else
  echo -e "\033[0;31mfailed\033[0m"
fi

if [[ $isortExit -ne 0 ]];
then
  echo
  echo "For an interactive auto fixer run"
  echo -e "\tisort --interactive ."
  echo "from ${git_dir}/src/"
  echo
fi

if [[ $isortExit -ne 0 || $flakeExit -ne 0 ]]
then
  exit 1
fi
