#!/bin/bash
set -e
PROJ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
find "$PROJ/src" -name "*.py" | while IFS= read -r f; do
    vim -c ':retab | :%s/\s\+$//e | :wq' "$f"
done
