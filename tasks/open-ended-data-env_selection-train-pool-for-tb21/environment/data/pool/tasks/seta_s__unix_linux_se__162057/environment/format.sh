#!/bin/bash
# Load environment settings
for f in /etc/profile.d/*.sh; do
    . "$f"
done

PROJECT="/home/project"

for file in "$PROJECT"/src/*.py; do
    emacs --batch --load "$PROJECT/.emacs.d/format-config.el" "$file" --eval "(progn (indent-region (point-min) (point-max)) (save-buffer))" 2>/dev/null
done
