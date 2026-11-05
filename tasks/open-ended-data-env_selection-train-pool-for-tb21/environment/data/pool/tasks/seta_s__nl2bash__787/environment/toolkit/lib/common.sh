# Common functions for ConfigCtl
# This file is sourced by other scripts

# Resolve library location
COMMON_DIR="$(dirname "$0")"
LIB_DIR="$COMMON_DIR"

# Source sub-libraries
source "$LIB_DIR/parser.sh"
source "$LIB_DIR/validator.sh"

# Logging functions
log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') $*"
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $*" >&2
}

log_warn() {
    echo "[WARN] $(date '+%Y-%m-%d %H:%M:%S') $*"
}

# Find toolkit root from any script
get_toolkit_root() {
    echo "$TOOLKIT_ROOT"
}

# Get output directory
get_output_dir() {
    local root
    root="$(get_toolkit_root)"
    echo "$root/output"
}
