#!/bin/bash
set -eu
declare -A PRIO=([10]=10 [12]=20 [13]=30)
for v in 10 12 13; do
    for tool in gcc g++; do
        [ -x "/usr/bin/$tool-$v" ] || { echo "missing /usr/bin/$tool-$v" >&2; exit 1; }
    done
done
for tool in gcc g++; do
    for v in $(printf '%s\n' "${!PRIO[@]}" | sort -n); do
        update-alternatives --quiet --install "/usr/bin/$tool" "$tool" "/usr/bin/$tool-$v" "${PRIO[$v]}"
    done
    update-alternatives --quiet --auto "$tool"
done
update-alternatives --quiet --install /usr/bin/cc cc /usr/bin/gcc 30
update-alternatives --quiet --install /usr/bin/c++ c++ /usr/bin/g++ 30
update-alternatives --quiet --auto cc
update-alternatives --quiet --auto c++
install -m 0755 /dev/stdin /app/switch-gcc.sh <<'SW'
#!/bin/bash
usage() { echo "Usage: ${0##*/} <version>   (e.g. ${0##*/} 12)" >&2; }

if [ $# -ne 1 ] || [ -z "$1" ]; then
    usage
    exit 1
fi
ver=${1#gcc-}
case $ver in
    *[!0-9.]*|.*|*.)
        echo "Error: '$1' is not a valid version number" >&2
        exit 1 ;;
esac

available() {
    update-alternatives --list "$1" 2>/dev/null | grep -Fxq "/usr/bin/$1-$ver"
}

missing=""
for t in gcc g++; do
    if [ ! -x "/usr/bin/$t-$ver" ]; then
        missing="$missing $t-$ver(not installed)"
    elif ! available "$t"; then
        missing="$missing $t-$ver(not registered with update-alternatives)"
    fi
done
if [ -n "$missing" ]; then
    echo "Error: version $ver is not available:$missing" >&2
    echo "Registered gcc versions:" >&2
    update-alternatives --list gcc 2>/dev/null | sed 's/^/  /' >&2
    exit 1
fi

for t in gcc g++; do
    if ! update-alternatives --set "$t" "/usr/bin/$t-$ver" >/dev/null; then
        echo "Error: failed to switch $t to $t-$ver" >&2
        exit 1
    fi
done

echo "Switched to gcc-$ver / g++-$ver"
gcc --version | head -n 1
g++ --version | head -n 1
exit 0
SW
gcc --version | head -n 1
g++ --version | head -n 1
cc --version | head -n 1
c++ --version | head -n 1
