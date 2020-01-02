#! /usr/bin/env bash

set -ex

export TESTING=True


# NOTE: Using Internal Field Separator (IFS) expansion syntax...
ptw --runner "pytest -s $* /app/app/tests"

#pytest "$*" /app/app/tests
