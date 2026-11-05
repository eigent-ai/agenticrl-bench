#!/bin/bash
if ! pg_isready -q 2>/dev/null; then
    pg_ctlcluster 16 main start
fi
