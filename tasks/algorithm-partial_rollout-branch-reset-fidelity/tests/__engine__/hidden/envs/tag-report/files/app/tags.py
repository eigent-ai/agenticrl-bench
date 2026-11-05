import sys

TAGS = {"backend", "frontend", "urgent", "billing", "infra", "docs", "mobile", "search", "growth", "security"}
if "--sorted" in sys.argv:
    print("\n".join(sorted(TAGS)))
else:
    for t in TAGS:
        print(t)
