#!/usr/bin/env python
# setup.py - Legacy build setup script
import os
import sys

def build():
    print("Running setup.py build...")

    # Create build directory
    os.makedirs("build", exist_ok=True)

    # Create a simple output file
    with open("build/output.txt", "w") as f:
        f.write("Build successful!\n")
        f.write(f"Python version: {sys.version}\n")

    print("setup.py build completed successfully!")
    return 0

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        sys.exit(build())
    else:
        print("Usage: python setup.py build")
        sys.exit(1)
