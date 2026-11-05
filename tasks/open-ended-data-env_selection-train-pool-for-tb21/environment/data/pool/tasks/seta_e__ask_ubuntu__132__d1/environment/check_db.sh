#!/bin/bash
if [ "$DB_FAIL" = "true" ]; then
  exit 1
else
  exit 0
fi
