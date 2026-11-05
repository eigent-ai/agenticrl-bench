#!/bin/bash
rm -f /root/.emacs
mkdir -p /root/.emacs.d
cat > /root/.emacs.d/init.el << 'EOF'
;; Disable tabs, use spaces
(setq-default indent-tabs-mode nil)

;; Set tab display width to 4
(setq-default tab-width 4)

;; Python indentation: 4 spaces
(setq python-indent-offset 4)

;; Enable line numbers globally
(global-display-line-numbers-mode 1)

;; Enable syntax highlighting globally
(global-font-lock-mode 1)

;; Enable electric-indent-mode for auto-indentation
(electric-indent-mode 1)

;; Clipboard integration via xclip
(require 'xclip)
(xclip-mode 1)

;; F2 to toggle electric-indent-mode
(global-set-key (kbd "<f2>") 'electric-indent-mode)
EOF
echo "Emacs configuration complete."
