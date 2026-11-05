#!/bin/bash
exec bash -c 'ulimit -n 64 && exec python "$@"' _ "$@"
