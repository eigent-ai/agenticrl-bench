#!/bin/bash
export PYTHONPATH="$PWD"
exec python -m pytest -p no:cacheprovider "$TESTS"
