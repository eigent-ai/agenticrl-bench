#!/bin/bash
# Wrapper for chattr that uses flag files in .attrs/ directories
# to simulate extended file attributes in environments where
# real chattr is not supported (e.g., Docker overlayfs)

mode=""
files=()

for arg in "$@"; do
    case "$arg" in
        +i) mode="add_immutable" ;;
        -i) mode="remove_immutable" ;;
        +a) mode="add_append_only" ;;
        -a) mode="remove_append_only" ;;
        -*) ;; # ignore other flags
        *) files+=("$arg") ;;
    esac
done

if [ -z "$mode" ]; then
    echo "chattr: Must use +/-[ia] to set/remove attributes" >&2
    exit 1
fi

for filepath in "${files[@]}"; do
    if [ ! -f "$filepath" ]; then
        echo "chattr: No such file or directory while trying to stat $filepath" >&2
        exit 1
    fi
    dir=$(dirname "$filepath")
    base=$(basename "$filepath")
    mkdir -p "$dir/.attrs"
    case "$mode" in
        add_immutable)    echo 1 > "$dir/.attrs/${base}.immutable" ;;
        remove_immutable) rm -f "$dir/.attrs/${base}.immutable" ;;
        add_append_only)  echo 1 > "$dir/.attrs/${base}.append_only" ;;
        remove_append_only) rm -f "$dir/.attrs/${base}.append_only" ;;
    esac
done
