"""Put the rollout dir on sys.path so the agent function imports by bare name, the way a rollout loads it
(``--custom-agent-function-path harbor_agent_function.run``)."""

import sys
from pathlib import Path

ROLLOUT_DIR = Path(__file__).resolve().parents[1]
if str(ROLLOUT_DIR) not in sys.path:
    sys.path.insert(0, str(ROLLOUT_DIR))
