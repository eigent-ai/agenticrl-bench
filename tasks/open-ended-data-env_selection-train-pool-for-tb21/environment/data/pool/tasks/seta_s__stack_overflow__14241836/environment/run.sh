#!/bin/bash
cd /opt/calutil && javac -d out src/*.java 2>&1 && java -cp out CalUtil "$@"
