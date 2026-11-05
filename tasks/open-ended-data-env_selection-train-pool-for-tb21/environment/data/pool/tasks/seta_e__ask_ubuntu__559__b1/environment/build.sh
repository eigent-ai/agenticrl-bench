#!/bin/bash

echo "Compiling application..."
mkdir -p /app/ci/build
gcc -o /app/ci/build/app /app/ci/src/app.c
if [ $? -eq 0 ]; then
    echo "Build successful!"
else
    echo "Build failed!"
    exit 1
fi
