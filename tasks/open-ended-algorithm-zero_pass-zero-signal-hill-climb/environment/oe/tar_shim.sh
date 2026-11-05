#!/bin/sh
# tar wrapper, installed as /usr/local/bin/tar (ahead of /usr/bin/tar on PATH; the image build checks it).
# GNU tar exits 1 when a file changed while it was being archived ("file changed as we read it", "file shrank"). The
# archive is still complete and readable, but Harbor treats any non-zero exit of its in-box `tar czf` as a lost
# artifact: one live writer (a log, a W&B dir) under /app would drop claims.txt and the manifest with it. In create mode
# exit 1 becomes 0 (the warning stays on stderr); every other exit status and every other mode is passed through.
# A checkpoint file that changed during the pack is caught by the verifier's manifest hash (invalid, not a score).
real=/usr/bin/tar
[ -x "$real" ] || real=/bin/tar
create=0
first=1
for a in "$@"; do
  case "$a" in
    --create) create=1 ;;
    --*) ;;
    -*c*) create=1 ;;
    *) [ "$first" = 1 ] && case "$a" in *c*) case "$a" in */*|*.*) ;; *) create=1 ;; esac ;; esac ;;
  esac
  first=0
done
"$real" "$@"
rc=$?
if [ "$create" = 1 ] && [ "$rc" = 1 ]; then
  echo "tar shim: exit 1 (files changed while archiving) -> 0; the archive is complete" >&2
  exit 0
fi
exit $rc
