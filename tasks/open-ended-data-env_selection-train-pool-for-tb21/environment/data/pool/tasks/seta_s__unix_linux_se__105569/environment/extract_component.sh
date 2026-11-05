#!/bin/bash
# Extract the component name from a build artifact path
# Expected path format: /builds/build_YYYYMMDD/component_vX.Y.Z/filename
basename "$1" | cut -d'_' -f1
