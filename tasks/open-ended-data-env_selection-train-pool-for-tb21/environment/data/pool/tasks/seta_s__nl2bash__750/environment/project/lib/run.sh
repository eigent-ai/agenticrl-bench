#!/bin/bash
# Run script for library operations

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/Helper.sh"

helper_greet
helper_validate "$1"
