#!/usr/bin/env bash
set -e

EXCLUDES=/etc/dpkg/dpkg.cfg.d/excludes

# Remove the man-page exclusion line using grep instead of sed
grep -v "path-exclude.*usr.share.man" "$EXCLUDES" > /tmp/excludes.new
mv /tmp/excludes.new "$EXCLUDES"

echo "=== excludes after fix ==="
cat "$EXCLUDES"

apt-get update -qq 2>&1 | tail -3

DEBIAN_FRONTEND=noninteractive apt-get install -y --reinstall man-db coreutils passwd util-linux 2>&1 | tail -5

echo "=== mandb output ==="
mandb 2>&1 | tail -10

echo "=== which man and type ==="
which man
ls -la "$(which man)"
ls -la "$(which man).REAL" 2>&1 || echo "no man.REAL"
head -3 "$(which man)"

echo "=== man ls test ==="
MANPAGER=cat man ls 2>&1 | head -5
echo "man ls exit: $?"

echo "=== man -k useradd test ==="
man -k useradd 2>&1 | head -3
