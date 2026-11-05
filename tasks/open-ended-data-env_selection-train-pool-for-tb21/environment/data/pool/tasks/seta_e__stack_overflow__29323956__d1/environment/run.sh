#!/bin/bash
cd /home/user/contrast-tool
if [ ! -d build ] || [ -z "$(ls -A build 2>/dev/null)" ]; then
    make build >&2
fi
java -cp build contrast.Main "$@"
