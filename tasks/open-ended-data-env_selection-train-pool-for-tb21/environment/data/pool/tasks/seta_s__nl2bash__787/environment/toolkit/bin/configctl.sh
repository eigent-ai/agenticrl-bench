#!/bin/bash
# ConfigCtl - Server Configuration Management Toolkit
# Usage: configctl <command> [args...]

set -euo pipefail

# Resolve script location
SCRIPT_DIR="$(dirname "$0")"
TOOLKIT_ROOT="$(dirname "$SCRIPT_DIR")"

# Source common library
source "$TOOLKIT_ROOT/lib/common.sh"

COMMAND="${1:-help}"
shift || true

case "$COMMAND" in
    audit)
        source "$TOOLKIT_ROOT/bin/modules/audit.sh"
        run_audit "$@"
        ;;
    apply)
        source "$TOOLKIT_ROOT/bin/modules/apply.sh"
        run_apply "$@"
        ;;
    rollback)
        source "$TOOLKIT_ROOT/bin/modules/rollback.sh"
        run_rollback "$@"
        ;;
    help)
        echo "Usage: configctl <audit|apply|rollback> [args...]"
        echo "  audit <target-dir>     - Audit configs against templates"
        echo "  apply <profile> <dir>  - Apply a configuration profile"
        echo "  rollback <dir>         - Rollback to previous config"
        ;;
    *)
        echo "Error: Unknown command '$COMMAND'" >&2
        exit 1
        ;;
esac
