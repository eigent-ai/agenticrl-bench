#!/bin/bash
set -eu
mkdir -p /root/.emacs.d
cat > /root/.emacs.d/init.el <<'EOF'
(setq-default indent-tabs-mode nil)
(setq-default tab-width 4)
(setq python-indent-offset 4)
(global-display-line-numbers-mode 1)
(global-font-lock-mode 1)
(electric-indent-mode 1)
(require 'xclip)
(xclip-mode 1)
(global-set-key (kbd "<f2>") 'electric-indent-mode)
EOF
