#!/bin/bash
# Release directory scaffolding script
# Creates new release directory structures from template

TEMPLATE="rel-0037"
TARGETS="rel-0038 rel-0039"
BASE_DIR="/srv/releases"

for target in $TARGETS; do
    echo "Scaffolding $target from $TEMPLATE..."
    find "$BASE_DIR/$TEMPLATE" -type d | sed "s/$TEMPLATE/$target/g" | xargs mkdir
    echo "Done: $target"
done

echo "Scaffolding complete."
