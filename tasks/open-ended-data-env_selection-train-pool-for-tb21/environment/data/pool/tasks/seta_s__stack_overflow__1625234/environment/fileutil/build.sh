#!/bin/bash
set -e
mkdir -p bin
javac -d bin src/FileUtil.java src/Main.java
echo "Build successful."
