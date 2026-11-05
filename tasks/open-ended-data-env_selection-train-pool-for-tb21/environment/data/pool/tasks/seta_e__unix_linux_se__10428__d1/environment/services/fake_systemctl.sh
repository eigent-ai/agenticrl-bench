#!/bin/bash
# Lightweight systemctl shim for containers that run without real systemd.
# Reads systemd-format unit files and manages processes via PID files.
#
# Supported operations:
#   start, stop, restart, is-active, status,
#   daemon-reload, enable, disable, mask, unmask, is-enabled, is-system-running

UNIT_DIR="/etc/systemd/system"
PID_DIR="/run/svc"
mkdir -p "$PID_DIR" 2>/dev/null || true

# ── helpers ──────────────────────────────────────────────────────────────────

unit_file() {
    echo "$UNIT_DIR/${1%.service}.service"
}

pid_file() {
    echo "$PID_DIR/${1%.service}.pid"
}

get_field() {
    # get_field FIELDNAME unit_file  →  value after first "FIELDNAME="
    grep -m1 "^${1}=" "$2" 2>/dev/null | cut -d'=' -f2-
}

svc_is_running() {
    local pidfile
    pidfile=$(pid_file "$1")
    [ -f "$pidfile" ] || return 1
    kill -0 "$(cat "$pidfile")" 2>/dev/null
}

svc_stop() {
    local name="${1%.service}"
    local pidfile
    pidfile=$(pid_file "$name")
    [ -f "$pidfile" ] || return 0
    local pid
    pid=$(cat "$pidfile")
    kill "$pid" 2>/dev/null || true
    sleep 0.5
    kill -9 "$pid" 2>/dev/null || true
    rm -f "$pidfile"
}

svc_start() {
    local name="${1%.service}"
    local unit
    unit=$(unit_file "$name")

    if [ ! -f "$unit" ]; then
        echo "Failed to start ${name}.service: unit file not found" >&2
        return 1
    fi

    local exec_start work_dir
    exec_start=$(get_field "ExecStart" "$unit")
    work_dir=$(get_field "WorkingDirectory" "$unit")

    if [ -z "$exec_start" ]; then
        echo "Failed to start ${name}.service: no ExecStart directive" >&2
        return 1
    fi

    # Build shell command; honour WorkingDirectory when present
    local cmd
    if [ -n "$work_dir" ]; then
        cmd="cd ${work_dir} && exec ${exec_start}"
    else
        cmd="exec ${exec_start}"
    fi

    # Launch in background; redirect I/O so it survives the parent exec session
    bash -c "$cmd" </dev/null >/dev/null 2>&1 &
    local bgpid=$!
    disown "$bgpid" 2>/dev/null || true
    echo "$bgpid" > "$(pid_file "$name")"

    # Quick liveness check
    sleep 0.4
    if ! svc_is_running "$name"; then
        rm -f "$(pid_file "$name")"
        echo "Failed to start ${name}.service: process exited immediately" >&2
        return 1
    fi
    return 0
}

# ── main dispatch ─────────────────────────────────────────────────────────────

SUBCMD="$1"
shift  # remaining args are service names (or options)

case "$SUBCMD" in
    start)
        svc_start "${1%.service}"
        ;;
    stop)
        svc_stop "${1%.service}"
        ;;
    restart)
        svc_stop "${1%.service}"
        sleep 0.3
        svc_start "${1%.service}"
        ;;
    is-active)
        if svc_is_running "${1%.service}"; then
            echo "active"
            exit 0
        else
            echo "inactive"
            exit 3
        fi
        ;;
    status)
        for raw_svc in "$@"; do
            svcname="${raw_svc%.service}"
            svcpid=$(cat "$(pid_file "$svcname")" 2>/dev/null)
            if svc_is_running "$svcname"; then
                printf "● %s.service\n   Active: active (running)\n   Main PID: %s\n\n" \
                    "$svcname" "$svcpid"
            else
                printf "● %s.service\n   Active: inactive (dead)\n\n" "$svcname"
            fi
        done
        ;;
    daemon-reload | enable | disable | mask | unmask | is-enabled | reenable)
        # These are no-ops: unit files are re-read fresh on each start/restart
        exit 0
        ;;
    is-system-running)
        echo "running"
        exit 0
        ;;
    --version)
        echo "systemd 252 (container shim)"
        exit 0
        ;;
    *)
        echo "systemctl: unknown operation '${SUBCMD}'" >&2
        exit 1
        ;;
esac
