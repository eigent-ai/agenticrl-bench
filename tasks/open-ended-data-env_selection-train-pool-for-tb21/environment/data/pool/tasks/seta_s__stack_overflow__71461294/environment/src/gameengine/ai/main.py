"""CLI entry point for AI simulation."""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from gameengine.ai.simulation import AISimulation
from gameengine.entities import Player, NPC, Monster, BossMonster


def run_simulation():
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    player = Player("Hero", hp=150, attack=12, defense=8)
    npc1 = NPC("Guard", hp=80, attack=6, defense=4, patrol_route=["gate", "market", "tavern"])
    npc2 = NPC("Merchant", hp=60, attack=3, defense=2, patrol_route=["shop", "warehouse"])
    monster1 = Monster("Goblin", hp=40, attack=8, defense=2, resistance=0.1)
    monster2 = Monster("Orc", hp=80, attack=12, defense=5, resistance=0.15)
    boss = BossMonster("Dragon", hp=500, attack=25, defense=15, resistance=0.3, shield=50)

    entities = [player, npc1, npc2, monster1, monster2, boss]

    sim = AISimulation(entities, max_ticks=20)
    report = sim.run()

    report_path = os.path.join(output_dir, "ai_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"AI simulation complete. Report: {report_path}")
    return report


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run_simulation":
        run_simulation()
    else:
        run_simulation()
