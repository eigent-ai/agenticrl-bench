# conftest.py - shared fixtures for mathcore tests
import sys
import os

# Ensure the bindings directory is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "bindings"))
