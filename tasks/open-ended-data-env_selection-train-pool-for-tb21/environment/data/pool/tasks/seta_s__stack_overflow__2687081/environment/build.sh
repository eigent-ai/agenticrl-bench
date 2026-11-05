#!/bin/bash
mkdir -p build
javac -Xlint:deprecation -d build src/*.java
