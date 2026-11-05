#!/bin/bash
case "$1" in
  --disk-usage)
    /usr/local/bin/journal-disk-usage
    ;;
  --vacuum-size=*)
    size="${1#--vacuum-size=}"
    size_mb="${size%M}"
    /usr/local/bin/journal-vacuum "$size_mb"
    ;;
  *)
    /usr/bin/journalctl.real "$@" 2>/dev/null || echo "journalctl: operation not supported in this environment"
    ;;
esac
