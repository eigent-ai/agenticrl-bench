#!/bin/bash
# Workspace path generator
# Generates colon-separated list of project directories

BASE_DIR="/home/developer/src"

find -L "$BASE_DIR" -type d | tr '\n' ':'
