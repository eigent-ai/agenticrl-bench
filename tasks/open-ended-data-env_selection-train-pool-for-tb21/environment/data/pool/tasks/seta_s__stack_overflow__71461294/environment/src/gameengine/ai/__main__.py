import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from gameengine.ai.main import run_simulation

if __name__ == "__main__":
    run_simulation()
