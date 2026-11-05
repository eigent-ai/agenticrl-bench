#!/bin/bash
set -e
conf="$HOME/.tmux.conf"
touch "$conf"
sed -i -E '/^[[:space:]]*set(-option)?[[:space:]]+.*(default-terminal|terminal-overrides)/d' "$conf"
cat >> "$conf" <<'TMUX'

# 24-bit colour: advertise a 256-colour terminfo inside tmux and pass RGB through to the outer terminal
set -g default-terminal "tmux-256color"
set -as terminal-overrides ',xterm-256color:RGB'
TMUX
rc="$HOME/.bashrc"
touch "$rc"
if grep -qE '^[[:space:]]*(export[[:space:]]+)?TERM=' "$rc"; then
    sed -i -E 's/^([[:space:]]*)(export[[:space:]]+)?TERM=.*/\1[ -n "$TMUX" ] || export TERM=xterm-256color/' "$rc"
fi
printf '\n# terminal colour support\nexport COLORTERM=truecolor\n[ -n "$TMUX" ] || export TERM=xterm-256color\n' >> "$rc"
