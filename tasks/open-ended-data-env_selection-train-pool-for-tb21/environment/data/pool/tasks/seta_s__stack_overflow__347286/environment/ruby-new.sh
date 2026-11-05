#!/bin/bash
if [ "$1" = "--version" ] || [ $# -eq 0 ]; then
    echo "ruby 3.2.0 (2022-12-25 revision a528908271) [x86_64-linux]"
else
    exec /bin/bash "$@"
fi
