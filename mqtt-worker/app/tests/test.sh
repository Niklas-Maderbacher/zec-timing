#!/usr/bin/env bash

set -e
set -x

coverage run --source=app -m pytest --disable-warnings --color=yes
coverage report --show-missing
coverage html --title "${@-coverage}"