#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/utils.sh"

main() {
    log_message "INFO" "Pipeline version ${PIPELINE_VERSION} starting"

    mkdir -p "${OUTPUT_DIR}"

    validate_input "${DATA_DIR}/input.csv" || exit 1

    bash "${SCRIPT_DIR}/workers/process_data.sh" || exit 1
    mark_stage_complete "processing"

    bash "${SCRIPT_DIR}/workers/generate_report.sh" || exit 1
    mark_stage_complete "reporting"

    log_message "INFO" "Completed stages:${COMPLETED_STAGES}"
    log_message "INFO" "Pipeline version ${PIPELINE_VERSION} completed successfully"
}

main
