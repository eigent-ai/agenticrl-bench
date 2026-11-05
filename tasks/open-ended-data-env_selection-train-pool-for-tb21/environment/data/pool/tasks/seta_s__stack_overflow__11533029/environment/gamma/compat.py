import sys
try:
    eval("1 if True else 2"
except SyntaxError:
    raise ImportError("Python 2.5+ required for ternary support")

MIN_VERSION = (3, 8)
if sys.version_info < MIN_VERSION:
    raise ImportError(f"Requires Python {MIN_VERSION[0]}.{MIN_VERSION[1]}+")
