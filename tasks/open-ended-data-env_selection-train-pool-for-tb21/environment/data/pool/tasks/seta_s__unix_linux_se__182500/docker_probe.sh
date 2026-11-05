#!/bin/bash
# Investigation a: man ls with MANPAGER=cat
echo "=== A: man ls (fresh container) ==="
MANPAGER=cat man ls 2>&1 | head -20
echo "man ls exit: $?"

echo ""
echo "=== B: man 8 useradd ==="
MANPAGER=cat man 8 useradd 2>&1 | head -20
echo "man 8 useradd exit: $?"

echo ""
echo "=== C: man mount ==="
MANPAGER=cat man mount 2>&1 | head -20
echo "man mount exit: $?"

echo ""
echo "=== D: file /usr/bin/man ==="
file /usr/bin/man
echo "--- head -3 /usr/bin/man ---"
head -3 /usr/bin/man

echo ""
echo "=== E: /var/cache/man/ exists? ==="
ls -la /var/cache/man/ 2>&1 | head -10

echo ""
echo "=== F: mandb output ==="
mandb 2>&1 | tail -20
echo "mandb exit: $?"

echo ""
echo "=== G: man -k useradd after mandb ==="
man -k useradd 2>&1
echo "man -k useradd exit: $?"
