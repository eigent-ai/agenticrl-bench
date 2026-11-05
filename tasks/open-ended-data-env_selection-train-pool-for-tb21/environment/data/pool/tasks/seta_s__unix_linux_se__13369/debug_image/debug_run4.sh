#!/bin/bash
# Isolated tests on fresh Xvfb displays

echo "=== Test 1: compose:ralt on FRESH Xvfb (with error reporting) ==="
Xvfb :81 -screen 0 1024x768x24 &
sleep 2
setxkbmap -display :81 -layout us -option compose:ralt
rc=$?
echo "setxkbmap rc: $rc"
cnt=$(xkbcomp :81 - 2>/dev/null | grep -c "Multi_key")
echo "Multi_key count: $cnt"
xkbcomp :81 - 2>/dev/null | grep -B2 -A5 "RALT" | grep -v "^--$" | head -20
kill %1 2>/dev/null; wait %1 2>/dev/null

echo ""
echo "=== Test 2: xkbcomp to stdout (not server) - does pc+custom_board include Multi_key? ==="
Xvfb :82 -screen 0 1024x768x24 &
sleep 2
cat << 'EOF' | xkbcomp -I/root/.xkb - - 2>/dev/null | grep -i "multi_key\|RALT\|ralt" | head -10
xkb_keymap {
    xkb_keycodes  { include "evdev+aliases(qwerty)" };
    xkb_types     { include "complete" };
    xkb_compat    { include "complete" };
    xkb_symbols   { include "pc+custom_board" };
    xkb_geometry  { include "pc(pc105)" };
};
EOF
kill %2 2>/dev/null; wait %2 2>/dev/null

echo ""
echo "=== Test 3: xkbcomp load to server - fresh display, explicit error check ==="
Xvfb :83 -screen 0 1024x768x24 &
sleep 2
echo "RALT before load:"
xkbcomp :83 - 2>/dev/null | grep -A3 "key <RALT>" | head -5
cat << 'EOF' | xkbcomp -I/root/.xkb - :83 2>&1 | grep -v "Warning\|XF86\|Could not\|XKEYBOARD\|xkbcomp reports\|not fatal"
xkb_keymap {
    xkb_keycodes  { include "evdev+aliases(qwerty)" };
    xkb_types     { include "complete" };
    xkb_compat    { include "complete" };
    xkb_symbols   { include "pc+custom_board" };
    xkb_geometry  { include "pc(pc105)" };
};
EOF
echo "xkbcomp load rc: $?"
echo "RALT after load:"
xkbcomp :83 - 2>/dev/null | grep -A3 "key <RALT>" | head -5
kill %3 2>/dev/null; wait %3 2>/dev/null

echo ""
echo "=== Test 4: setxkbmap pipeline on fresh display, with error reporting ==="
Xvfb :84 -screen 0 1024x768x24 &
sleep 2
echo "RALT before:"
xkbcomp :84 - 2>/dev/null | grep -A3 "key <RALT>" | head -5

DISPLAY=:84 setxkbmap custom_board -print | xkbcomp -I/root/.xkb - :84 2>&1 | grep -v "Warning\|XF86\|Could not\|XKEYBOARD\|xkbcomp reports\|not fatal"
echo "pipeline rc: $?"

echo "RALT after pipeline:"
xkbcomp :84 - 2>/dev/null | grep -A3 "key <RALT>" | head -5
kill %4 2>/dev/null; wait %4 2>/dev/null

echo ""
echo "=== Test 5: Xvfb with -noxkb, then xmodmap ==="
Xvfb :85 -screen 0 1024x768x24 -noxkb &
sleep 2
echo "keycode 135 before:"
xmodmap -display :85 -pke | grep "keycode 135 "
echo "keycode 135 = Super_R" | xmodmap -display :85 -
echo "xmodmap rc: $?"
echo "keycode 135 after:"
xmodmap -display :85 -pke | grep "keycode 135 "
kill %5 2>/dev/null; wait %5 2>/dev/null

echo ""
echo "=== Test 6: xmodmap with -noxkb Xvfb, full xmodmaprc ==="
Xvfb :86 -screen 0 1024x768x24 -noxkb &
sleep 2
xmodmap -display :86 /root/.xmodmaprc 2>&1
echo "xmodmap rc: $?"
xmodmap -display :86 -pke | grep "keycode 13[34567] "
kill %6 2>/dev/null; wait %6 2>/dev/null
