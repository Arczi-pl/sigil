#!/usr/bin/env bash

# shellcheck source=scripts/logger.sh
source "$(dirname "$(dirname "$(readlink -f "$0")")")/logger.sh" 2>/dev/null || source "$(dirname "$(readlink -f "$0")")/scripts/logger.sh" || exit 1
# shellcheck source=scripts/config.sh
source "$(dirname "$(dirname "$(readlink -f "$0")")")/config.sh" 2>/dev/null || source "$(dirname "$(readlink -f "$0")")/scripts/config.sh" || exit 1

create_python_venv() {
	local venv_path
	local requirements_path

	venv_path="${1}"
	requirements_path="${2}"

	note "Creating python venv in ${venv_path}"
	python -m venv "${venv_path}" || exit 1
	source -- "${venv_path}/bin/activate" || exit 1

	note "Installing requirements from ${requirements_path}"
	python -m pip -q --disable-pip-version-check install -r "${requirements_path}" \
		--retries 3 \
		--timeout 10 || exit 1
}
