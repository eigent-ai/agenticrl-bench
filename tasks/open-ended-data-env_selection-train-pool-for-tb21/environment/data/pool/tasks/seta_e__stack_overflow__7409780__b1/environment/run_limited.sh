#!/bin/bash
exec bash -c 'ulimit -n 64 && exec ruby "$@"' _ "$@"
