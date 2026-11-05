#!/bin/bash
set -eu
declare -A prio=([10]=10 [12]=20 [13]=30)
for v in 13 10 12; do
    update-alternatives --quiet \
        --install /usr/bin/gcc gcc "/usr/bin/gcc-$v" "${prio[$v]}" \
        --slave /usr/bin/cpp cpp "/usr/bin/cpp-$v" \
        --slave /usr/bin/gcov gcov "/usr/bin/gcov-$v" \
        --slave /usr/bin/gcc-ar gcc-ar "/usr/bin/gcc-ar-$v" \
        --slave /usr/bin/gcc-nm gcc-nm "/usr/bin/gcc-nm-$v" \
        --slave /usr/bin/gcc-ranlib gcc-ranlib "/usr/bin/gcc-ranlib-$v"
    update-alternatives --quiet --install /usr/bin/g++ g++ "/usr/bin/g++-$v" "${prio[$v]}"
done
update-alternatives --quiet --install /usr/bin/cc cc /usr/bin/gcc 20
update-alternatives --quiet --install /usr/bin/c++ c++ /usr/bin/g++ 20
update-alternatives --quiet --set gcc /usr/bin/gcc-13
update-alternatives --quiet --set g++ /usr/bin/g++-13
cat > /app/switch-gcc.sh <<'EOF'
#!/usr/bin/env bash
# switch-gcc.sh VERSION -- select gcc-VERSION and g++-VERSION as the system gcc/g++.
# VERSION may be given as "12" or "gcc-12".

prog=${0##*/}
die() { echo "$prog: $*" >&2; exit 1; }

[ $# -eq 1 ] || die "usage: $prog VERSION (for example: $prog 13)"
ver=${1#gcc-}
case $ver in
    ''|*[!0-9]*) die "invalid version '$1'" ;;
esac

for tool in gcc g++; do
    if [ ! -x "/usr/bin/$tool-$ver" ]; then
        avail=$(update-alternatives --list gcc 2>/dev/null | sed -n 's|^/usr/bin/gcc-||p' | sort -n | tr '\n' ' ')
        die "$tool-$ver is not installed (available: ${avail:-none})"
    fi
    update-alternatives --list "$tool" 2>/dev/null | grep -qx "/usr/bin/$tool-$ver" \
        || die "$tool-$ver is not registered with update-alternatives"
done

prev_gcc=$(readlink -f /etc/alternatives/gcc 2>/dev/null)
update-alternatives --quiet --set gcc "/usr/bin/gcc-$ver" || die "failed to select gcc-$ver"
if ! update-alternatives --quiet --set g++ "/usr/bin/g++-$ver"; then
    # keep the pair consistent
    [ -n "$prev_gcc" ] && update-alternatives --quiet --set gcc "$prev_gcc"
    die "failed to select g++-$ver"
fi

[ "$(gcc -dumpversion | cut -d. -f1)" = "$ver" ] && [ "$(g++ -dumpversion | cut -d. -f1)" = "$ver" ] \
    || die "selection did not take effect"
exit 0
EOF
chmod 0700 /app/switch-gcc.sh
ln -sfn /app/switch-gcc.sh /usr/local/bin/switch-gcc.sh
gcc --version | head -n1
g++ --version | head -n1
cc --version | head -n1
c++ --version | head -n1
