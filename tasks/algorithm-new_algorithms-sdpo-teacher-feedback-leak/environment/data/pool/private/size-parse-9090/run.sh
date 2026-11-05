#!/bin/bash
export PYTHONPATH="$PWD"
exec python -m unittest discover -s "$TESTS" -t "$TESTS" -p 'test_*.py'
