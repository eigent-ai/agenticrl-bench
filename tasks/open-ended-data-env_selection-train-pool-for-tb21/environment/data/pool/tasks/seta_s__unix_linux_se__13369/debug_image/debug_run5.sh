#!/bin/bash
# Test reliable verification approaches

echo "=== Test A: Compile pc+custom_board to file then decompile to text ==="
cat << 'EOF' > /tmp/minimal.xkb
xkb_keymap {
    xkb_keycodes  { include "evdev+aliases(qwerty)" };
    xkb_types     { include "complete" };
    xkb_compat    { include "complete" };
    xkb_symbols   { include "pc+custom_board" };
    xkb_geometry  { include "pc(pc105)" };
};
EOF
xkbcomp -I/root/.xkb /tmp/minimal.xkb /tmp/minimal.xkm 2>&1 | grep -v "Warning\|XF86\|Could not\|Ignored\|not fatal\|XKEYBOARD\|xkbcomp reports" | head -20
echo "compile rc: $?"
if [ -f /tmp/minimal.xkm ]; then
    echo "=== Decompile to text ==="
    xkbcomp /tmp/minimal.xkm /tmp/minimal_out.xkb 2>/dev/null
    echo "decompile rc: $?"
    grep -A5 "RALT" /tmp/minimal_out.xkb | head -15
    grep -c "Multi_key" /tmp/minimal_out.xkb && echo "Multi_key FOUND in decompiled text" || echo "Multi_key NOT found"
else
    echo "No .xkm file created"
fi

echo ""
echo "=== Test B: Compile full chain (with inet) to file then decompile ==="
Xvfb :91 -screen 0 1024x768x24 &
sleep 2
DISPLAY=:91 setxkbmap custom_board -print > /tmp/full_chain.xkb 2>/dev/null
echo "setxkbmap -print output:"
cat /tmp/full_chain.xkb
xkbcomp -I/root/.xkb /tmp/full_chain.xkb /tmp/full_chain.xkm 2>&1 | grep -v "Warning\|XF86\|Could not\|Ignored\|not fatal\|XKEYBOARD\|xkbcomp reports" | head -5
echo "compile rc: $?"
if [ -f /tmp/full_chain.xkm ]; then
    xkbcomp /tmp/full_chain.xkm /tmp/full_chain_out.xkb 2>/dev/null
    echo "decompile rc: $?"
    grep -A3 "key.*RALT" /tmp/full_chain_out.xkb | head -10
    grep -c "Multi_key" /tmp/full_chain_out.xkb && echo "Multi_key FOUND" || echo "Multi_key NOT found"
fi
kill %1 2>/dev/null; wait %1 2>/dev/null

echo ""
echo "=== Test C: Binary output contains Multi_key? ==="
echo "Compiling minimal (pc+custom_board) to stdout binary:"
xkbcomp -I/root/.xkb /tmp/minimal.xkb - 2>/dev/null | strings | grep -i "multi_key" | head -5
echo "strings grep exit: $?"

echo ""
echo "=== Test D: xmodmap -n (dry run) to check what would happen ==="
Xvfb :92 -screen 0 1024x768x24 &
sleep 2
echo "xmodmap -n /root/.xmodmaprc output:"
xmodmap -display :92 -n /root/.xmodmaprc 2>&1
echo "xmodmap -n rc: $?"
kill %2 2>/dev/null; wait %2 2>/dev/null

echo ""
echo "=== Test E: Check setxkbmap -print output contains custom_board ==="
Xvfb :93 -screen 0 1024x768x24 &
sleep 2
out=$(DISPLAY=:93 setxkbmap custom_board -print 2>/dev/null)
echo "setxkbmap output:"
echo "$out"
echo "$out" | grep -c "custom_board" && echo "custom_board in setxkbmap output" || echo "NOT found"
kill %3 2>/dev/null; wait %3 2>/dev/null

echo ""
echo "=== Test F: Check what xkbcomp produces when file NOT found (NOP state) ==="
# Simulate NOP: file only at /root/.xkb/custom_board (not in symbols/)
mkdir -p /tmp/fake_xkb
cp /root/.xkb/custom_board /tmp/fake_xkb/custom_board  # wrong location, not in symbols/
Xvfb :94 -screen 0 1024x768x24 &
sleep 2
out=$(DISPLAY=:94 setxkbmap custom_board -print 2>/dev/null | xkbcomp -I/tmp/fake_xkb - /tmp/nop_out.xkm 2>&1)
rc=$?
echo "Pipeline rc (NOP simulation): $rc"
echo "stderr output:"
echo "$out" | head -5
echo "Can't find file present: $(echo "$out" | grep -c "Can.t find file")"
kill %4 2>/dev/null; wait %4 2>/dev/null
