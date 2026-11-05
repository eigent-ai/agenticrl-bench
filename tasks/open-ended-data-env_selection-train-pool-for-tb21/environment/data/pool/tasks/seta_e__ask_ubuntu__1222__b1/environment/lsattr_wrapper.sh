#!/bin/bash
# Wrapper for lsattr that uses flag files in .attrs/ directories
# to simulate extended file attributes in environments where
# real chattr/lsattr is not supported (e.g., Docker overlayfs)

print_attrs() {
    local filepath="$1"
    local base dir attrs
    base=$(basename "$filepath")
    dir=$(dirname "$filepath")
    attrs="-------------------"
    if [ -f "$dir/.attrs/${base}.immutable" ]; then
        attrs="----i--------------"
    fi
    if [ -f "$dir/.attrs/${base}.append_only" ]; then
        attrs="-----a-------------"
    fi
    echo "$attrs $filepath"
}

# Parse arguments
files=()
for arg in "$@"; do
    case "$arg" in
        -*) ;; # ignore flags like -R, -d, -a, -v
        *) files+=("$arg") ;;
    esac
done

if [ ${#files[@]} -eq 0 ]; then
    files=(".")
fi

for path in "${files[@]}"; do
    if [ -d "$path" ]; then
        for f in "$path"/*; do
            [ -f "$f" ] || continue
            print_attrs "$f"
        done
    elif [ -f "$path" ]; then
        print_attrs "$path"
    else
        echo "lsattr: No such file or directory while trying to stat $path" >&2
    fi
done
