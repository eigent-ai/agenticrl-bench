#!/bin/bash
# Rollback module for ConfigCtl

if [[ -z "${TOOLKIT_ROOT:-}" ]]; then
    SCRIPT_DIR="$(dirname "$0")"
    TOOLKIT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
    source "$TOOLKIT_ROOT/lib/common.sh"
fi

run_rollback() {
    local target_dir="${1:?Usage: configctl rollback <target-dir>}"

    local output_dir
    output_dir="$(get_output_dir)/applied"

    if [[ ! -d "$output_dir" ]]; then
        log_error "No applied configs found to rollback"
        return 1
    fi

    local manifest="$output_dir/manifest.txt"
    if [[ ! -f "$manifest" ]]; then
        log_error "No manifest found — cannot rollback"
        return 1
    fi

    log_info "Rolling back applied configs from $output_dir"
    rm -f "$output_dir"/*.conf "$output_dir"/*.txt
    log_info "Rollback complete"
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    run_rollback "$@"
fi
