#!/bin/bash
# Check if inet(evdev) defines RALT - and test workarounds

echo "=== inet symbols file - RALT references ==="
grep -n "RALT\|ralt" /usr/share/X11/xkb/symbols/inet 2>/dev/null | head -20
echo ""

echo "=== Does inet(evdev) define key RALT? ==="
# Extract the evdev section from inet
awk '/xkb_symbols "evdev"/,/^};/' /usr/share/X11/xkb/symbols/inet 2>/dev/null | grep -i "ralt\|RALT" | head -10
echo ""

echo "=== level3 symbols - RALT? ==="
grep -n "RALT" /usr/share/X11/xkb/symbols/level3 2>/dev/null | head -10
echo ""

# Start Xvfb
Xvfb :91 -screen 0 1024x768x24 &
sleep 3
export DISPLAY=:91
export HOME=/root

echo "=== WORKAROUND 1: custom_board at END of include chain ==="
setxkbmap custom_board -print | sed 's/include "pc+custom_board+inet(evdev)"/include "pc+inet(evdev)+custom_board"/' | xkbcomp -I/root/.xkb - :91 2>/dev/null
cnt=$(xkbcomp :91 - 2>/dev/null | grep -c "Multi_key")
echo "Multi_key count (chain reversed): $cnt"
echo ""

echo "=== WORKAROUND 2: custom_board only (no inet/evdev) ==="
echo 'xkb_keymap { xkb_keycodes { include "evdev+aliases(qwerty)" }; xkb_types { include "complete" }; xkb_compat { include "complete" }; xkb_symbols { include "pc+custom_board" }; xkb_geometry { include "pc(pc105)" }; }' | xkbcomp -I/root/.xkb - :91 2>/dev/null
cnt=$(xkbcomp :91 - 2>/dev/null | grep -c "Multi_key")
echo "Multi_key count (pc+custom_board only): $cnt"
echo ""

echo "=== WORKAROUND 3: setxkbmap -option compose:ralt ==="
setxkbmap -layout us -option compose:ralt 2>/dev/null
cnt=$(xkbcomp :91 - 2>/dev/null | grep -c "Multi_key")
echo "Multi_key count (compose:ralt option): $cnt"
echo ""

echo "=== WORKAROUND 4: xmodmap with force ==="
echo "keycode 108 = Multi_key" | xmodmap - 2>/dev/null
xmodmap -pke 2>/dev/null | grep "keycode 108 "
echo ""

echo "=== WORKAROUND 5: xdotool / xev alternative check ==="
# Check if xdotool available
which xdotool 2>/dev/null || echo "xdotool not available"

echo ""
echo "=== What keycode is RALT? ==="
xmodmap -pke 2>/dev/null | grep -i "alt_r\|ralt" | head -10
echo ""

echo "=== Test xmodmap on keycode 108 (RALT keycode) ==="
echo "keycode 108 = Super_R" | xmodmap - 2>/dev/null
echo "xmodmap exit: $?"
xmodmap -pke 2>/dev/null | grep "keycode 108 "
