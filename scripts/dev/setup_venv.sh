#!/usr/bin/env bash

# shellcheck source=scripts/utils.sh
source "$(dirname "$(dirname "$(readlink -f "$0")")")/utils.sh" || exit 1

create_python_venv "${VENV_PATH}" "${REQUIREMENTS_PATH}" || exit 1

warn "Remember to \`source ${VENV_PATH}/bin/activate\` before running any script!"
