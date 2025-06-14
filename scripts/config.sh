#!/usr/bin/env bash
# shellcheck disable=SC2034

REPOSITORY_PATH="$(realpath "$(dirname "$(realpath "${BASH_SOURCE[0]}")")/..")"
SRC_PATH="${REPOSITORY_PATH}/src"
TESTS_PATH="${REPOSITORY_PATH}/src/tests"
REQUIREMENTS_PATH="${REPOSITORY_PATH}/requirements.txt"
PYPROJECT_PATH="${REPOSITORY_PATH}/pyproject.toml"
VENV_PATH="${REPOSITORY_PATH}/.venv"
