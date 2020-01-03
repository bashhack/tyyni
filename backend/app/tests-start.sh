#! /usr/bin/env bash

set -ex

export TESTING=True


# NOTE: Using Internal Field Separator (IFS) expansion syntax...
# ptw -w --runner "pytest -s $* /app/app/tests"
# NOTE:
#   - DB errors: https://github.com/joeyespo/pytest-watch/issues/23
#   - Follow-up: https://github.com/joeyespo/pytest-watch/issues/36

pytest "$*" /app/app/tests
