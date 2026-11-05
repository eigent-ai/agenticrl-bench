#!/bin/bash
set -eu
printf '%s\n' 'set completion-ignore-case On' > /etc/inputrc
printf '%s\n' '$include /etc/inputrc' 'set completion-ignore-case On' > ~/.inputrc
