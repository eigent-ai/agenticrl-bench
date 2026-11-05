import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from gameengine.persistence.main import cmd_save, cmd_load

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m gameengine.persistence [save|load]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "save":
        cmd_save()
    elif cmd == "load":
        cmd_load()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
