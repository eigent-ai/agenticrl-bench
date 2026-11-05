#!/bin/bash
cat > /app/filter.py <<'PY'
import re, sys
p = sys.argv[1]
s = open(p).read()
s = re.sub(r"(?is)<script\b.*?</script\s*>", "", s)
open(p, "w").write(s)
PY
