#!/usr/bin/env bash

# shellcheck source=scripts/utils.sh
source "$(dirname "$(readlink -f "$0")")/scripts/utils.sh" || exit 1

PYTHONPATH=$REPOSITORY_PATH "${REPOSITORY_PATH}/src/sigil.py" \
    --input "examples/lorem_ipsum.txt" \
    --output "examples/lorem_ipsum_output.txt" \
    --signature "created by Artur Sikorski"

PYTHONPATH=$REPOSITORY_PATH "${REPOSITORY_PATH}/src/learn.py" \
    --file "examples/lorem_ipsum_output.txt"

PYTHONPATH=$REPOSITORY_PATH "${REPOSITORY_PATH}/src/sigil_extractor.py" \
    --input "examples/lorem_ipsum_output.txt"
