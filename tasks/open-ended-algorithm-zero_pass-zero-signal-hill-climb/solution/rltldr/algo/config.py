"""Plug-in settings (config.json next to this file). Group size and tasks per step come from the job's Miles args."""
import json
from pathlib import Path

CFG = json.loads((Path(__file__).resolve().parent / "config.json").read_text())
