#! /usr/bin/env bash

set -ex

python /app/app/tests_pre_start.py

# NOTE: Using Internal Field Separator (IFS) expansion syntax...
ptw --runner "pytest --testmon $* /app/app/tests"

# pytest "$*" /app/app/tests