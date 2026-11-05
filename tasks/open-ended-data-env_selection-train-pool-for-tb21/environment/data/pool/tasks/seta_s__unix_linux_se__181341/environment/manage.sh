#!/bin/bash
#
# Sandbox Process Management Script
# Manages isolated process execution under the sandbox user account
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/config.env"

LOG_PREFIX="[sandbox-mgr]"

log_info() {
    echo "$LOG_PREFIX INFO: $*"
}

log_error() {
    echo "$LOG_PREFIX ERROR: $*" >&2
}

check_subid_file() {
    local file="$1"
    local label="$2"
    local errors=0

    if [ ! -f "$file" ]; then
        log_error "$label file $file not found"
        return 1
    fi

    local line_num=0
    while IFS=' ' read -r user start count; do
        line_num=$((line_num + 1))
        [ -z "$user" ] && continue

        if [ -z "$start" ] || [ -z "$count" ]; then
            log_error "$label line $line_num: malformed entry (user=$user)"
            errors=$((errors + 1))
            continue
        fi

        if ! [[ "$start" =~ ^[0-9]+$ ]] || ! [[ "$count" =~ ^[0-9]+$ ]]; then
            log_error "$label line $line_num: non-numeric start/count (start=$start, count=$count)"
            errors=$((errors + 1))
        fi
    done < "$file"

    return $errors
}

check_subid_overlaps() {
    local file="$1"
    local label="$2"

    local -a users=()
    local -a starts=()
    local -a counts=()

    cat "$file" | while read line; do
        [ -z "$line" ] && continue
        local user start count
        IFS=':' read -r user start count <<< "$line"
        [ -z "$count" ] && continue
        users+=("$user")
        starts+=("$start")
        counts+=("$count")
    done

    local num_entries=${#users[@]}
    local i j
    for ((i=0; i<num_entries; i++)); do
        for ((j=i+1; j<num_entries; j++)); do
            local s1=${starts[$i]} c1=${counts[$i]}
            local s2=${starts[$j]} c2=${counts[$j]}
            local e1=$((s1 + c1))
            local e2=$((s2 + c2))
            if [ "$s1" -lt "$e2" ] && [ "$s2" -lt "$e1" ]; then
                log_error "$label: overlapping ranges for ${users[$i]} and ${users[$j]}"
                return 1
            fi
        done
    done

    log_info "$label: no overlapping ranges detected"
    return 0
}

check_sandbox_user_entry() {
    local file="$1"
    local label="$2"

    if ! grep -q "^${SANDBOX_USER}:" "$file"; then
        log_error "$label: no entry found for user '$SANDBOX_USER'"
        return 1
    fi

    log_info "$label: entry found for '$SANDBOX_USER'"
    return 0
}

check_config_consistency() {
    local subuid_file="/etc/subuid"

    local sandbox_line
    sandbox_line=$(grep "^${SANDBOX_USER}:" "$subuid_file" 2>/dev/null || true)
    if [ -z "$sandbox_line" ]; then
        log_error "config consistency: no subuid entry for $SANDBOX_USER"
        return 1
    fi

    local file_start file_count
    IFS=':' read -r _ file_start file_count <<< "$sandbox_line"

    if [ "$file_start" != "$SANDBOX_UID_START" ]; then
        log_error "config consistency: SANDBOX_UID_START ($SANDBOX_UID_START) != subuid start ($file_start)"
        return 1
    fi

    if [ "$file_count" != "$SANDBOX_UID_COUNT" ]; then
        log_error "config consistency: SANDBOX_UID_COUNT ($SANDBOX_UID_COUNT) != subuid count ($file_count)"
        return 1
    fi

    log_info "config consistency: config.env matches subuid entries"
    return 0
}

check_sudoers() {
    local sudoers_file="/etc/sudoers.d/monitors"

    if [ ! -f "$sudoers_file" ]; then
        log_error "sudoers: $sudoers_file not found"
        return 1
    fi

    if ! visudo -c -f "$sudoers_file" > /dev/null 2>&1; then
        log_error "sudoers: syntax error in $sudoers_file"
        return 1
    fi

    if ! grep -q "NOPASSWD:" "$sudoers_file"; then
        log_error "sudoers: NOPASSWD tag missing in $sudoers_file"
        return 1
    fi

    if ! grep -q "/bin/kill" "$sudoers_file"; then
        log_error "sudoers: /bin/kill not found in $sudoers_file"
        return 1
    fi

    log_info "sudoers: configuration valid"
    return 0
}

check_sysctl() {
    local sysctl_file="/etc/sysctl.d/99-userns.conf"

    if [ ! -f "$sysctl_file" ]; then
        log_error "sysctl: $sysctl_file not found"
        return 1
    fi

    local ns_val
    ns_val=$(grep "user.max_user_namespaces" "$sysctl_file" | awk -F'=' '{print $2}' | tr -d ' ')

    if [ -z "$ns_val" ]; then
        log_error "sysctl: user.max_user_namespaces not set"
        return 1
    fi

    if [ "$ns_val" -le 0 ] 2>/dev/null; then
        log_error "sysctl: user.max_user_namespaces is $ns_val (must be > 0)"
        return 1
    fi

    log_info "sysctl: user.max_user_namespaces = $ns_val"
    return 0
}

do_validate() {
    local failures=0

    log_info "Starting validation..."

    check_subid_file /etc/subuid "subuid" || failures=$((failures + 1))
    check_subid_file /etc/subgid "subgid" || failures=$((failures + 1))
    check_subid_overlaps /etc/subuid "subuid" || failures=$((failures + 1))
    check_subid_overlaps /etc/subgid "subgid" || failures=$((failures + 1))
    check_sandbox_user_entry /etc/subuid "subuid" || failures=$((failures + 1))
    check_sandbox_user_entry /etc/subgid "subgid" || failures=$((failures + 1))
    check_config_consistency || failures=$((failures + 1))
    check_sudoers || failures=$((failures + 1))
    check_sysctl || failures=$((failures + 1))

    if [ "$failures" -gt 0 ]; then
        log_error "Validation failed with $failures error(s)"
        return 1
    fi

    log_info "All validation checks passed"
    return 0
}

do_run() {
    local cmd="$1"

    if [ -z "$cmd" ]; then
        log_error "Usage: $0 run <script>"
        return 1
    fi

    if [ ! -f "$cmd" ]; then
        log_error "Script not found: $cmd"
        return 1
    fi

    log_info "Running validation before execution..."
    do_validate || { log_error "Validation failed, aborting run"; return 1; }

    local output_dir=$OUTPUT_DIR
    mkdir -p $output_dir
    chmod 777 $output_dir

    local run_output_dir="/opt/sandbox/output"
    mkdir -p "$run_output_dir"
    chmod 777 "$run_output_dir"

    log_info "Executing $cmd as $SANDBOX_USER..."
    su sandbox -c "bash $cmd $run_output_dir/result.txt"
    local rc=$?

    if [ $rc -eq 0 ]; then
        log_info "Execution completed successfully"
    else
        log_error "Execution failed with exit code $rc"
    fi

    return $rc
}

case "${1:-}" in
    validate)
        do_validate
        ;;
    run)
        do_run "$2"
        ;;
    *)
        echo "Usage: $0 {validate|run <script>}"
        exit 1
        ;;
esac
