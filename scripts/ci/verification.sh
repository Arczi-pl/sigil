#!/usr/bin/env bash

# shellcheck source=scripts/utils.sh
source "$(dirname "$(dirname "$(readlink -f "$0")")")/utils.sh" || exit 1

check_shell() {
	local exit_code=0
	local addopts=""

	[[ " $* " =~ " --skip-venv " ]] || create_python_venv "${VENV_PATH}" "${REQUIREMENTS_PATH}" || exit 1
	[[ " $* " =~ " --pre-commit " ]] && addopts="-w"
	# shellcheck disable=SC2046
	if ! shellcheck -P "${REPOSITORY_PATH}" -x -C -s bash $(find "${REPOSITORY_PATH}/scripts" -iname "*.sh" -type f); then
		exit_code=1
	fi
	# shellcheck disable=SC2046
	if ! shfmt -d $addopts "${REPOSITORY_PATH}/scripts"; then
		exit_code=1
	fi
	exit $exit_code
}

check_ruff() {
	local addopts=""
	[[ " $* " =~ " --skip-venv " ]] || create_python_venv "${VENV_PATH}" "${REQUIREMENTS_PATH}" || exit 1
	[[ " $* " =~ " --fix " ]] && addopts="--fix"
	ruff check $addopts "${REPOSITORY_PATH}/src"
}

check_ruff_format() {
	local addopts=""
	[[ " $* " =~ " --skip-venv " ]] || create_python_venv "${VENV_PATH}" "${REQUIREMENTS_PATH}" || exit 1
	[[ " $* " =~ " --fix " ]] || addopts="--check --diff"
	# shellcheck disable=SC2086
	ruff format $addopts "${REPOSITORY_PATH}/src"
}

check_mypy() {
	[[ " $* " =~ " --skip-venv " ]] || create_python_venv "${VENV_PATH}" "${REQUIREMENTS_PATH}" || exit 1
	mypy "${REPOSITORY_PATH}/src"
}

check_requirements() {
	local exit_code=0

	create_python_venv "${REPOSITORY_PATH}/.tmp_venv" "${REQUIREMENTS_PATH}" || exit 1
	if ! diff <(python -m pip freeze) "${REQUIREMENTS_PATH}"; then
		err "Requirements not matched for ${REQUIREMENTS_PATH}"
		exit_code=1
	fi
	deactivate
	rm -rf "${REPOSITORY_PATH}/.tmp_venv"

	if [ $exit_code -eq 0 ]; then
		hint "All requirements matched!"
	fi
	exit $exit_code
}

check_pytest() {
	local test_file
	[[ " $* " =~ " --skip-venv " ]] || create_python_venv "${VENV_PATH}" "${REQUIREMENTS_PATH}" || exit 1
	[[ " $* " =~ " --test-file " ]] && test_file=$(sed -n 's/.*--test-file \([^ ]*\).*/\1/p' <<<"$*")
	cd "${REPOSITORY_PATH}" || exit 1
	coverage run --rcfile="${PYPROJECT_PATH}" -m pytest -vvv --config-file "${PYPROJECT_PATH}" "${TESTS_PATH}/${test_file}"
	[[ " $* " =~ " --test-file " ]] || coverage html --rcfile="${PYPROJECT_PATH}" --directory "${REPOSITORY_PATH}/coverage_report"
}

"$@"
