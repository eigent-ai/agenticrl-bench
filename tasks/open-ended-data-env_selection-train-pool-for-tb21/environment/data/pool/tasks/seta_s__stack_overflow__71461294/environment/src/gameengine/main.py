"""Main entry point for the game engine demo."""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gameengine.config import load_config
from gameengine.entities import Player, NPC, Monster, BossMonster
from gameengine.systems.events import EventDispatcher, Event
from gameengine.systems.combat import CombatSystem
from gameengine.systems.interaction import InteractionSystem


def load_content(content_dir):
    """Load game content from YAML files."""
    import yaml
    content = {}
    for fname in os.listdir(content_dir):
        if fname.endswith(".yaml") or fname.endswith(".yml"):
            path = os.path.join(content_dir, fname)
            with open(path, "r") as f:
                content[fname.replace(".yaml", "").replace(".yml", "")] = yaml.safe_load(f)
    return content


def create_entities_from_content(content):
    """Create entity instances from loaded content data."""
    entities = []
    entity_defs = content.get("entities", {}).get("entities", [])
    for edef in entity_defs:
        etype = edef.get("type", "npc")
        kwargs = {k: v for k, v in edef.items() if k not in ("name", "type", "hp", "attack", "defense")}
        if etype == "player":
            e = Player(edef["name"], hp=edef.get("hp", 150), attack=edef.get("attack", 12), defense=edef.get("defense", 8), **kwargs)
        elif etype == "npc":
            e = NPC(edef["name"], hp=edef.get("hp", 80), attack=edef.get("attack", 6), defense=edef.get("defense", 4), **kwargs)
        elif etype == "monster":
            e = Monster(edef["name"], hp=edef.get("hp", 60), attack=edef.get("attack", 14), defense=edef.get("defense", 3), **kwargs)
        elif etype == "boss_monster":
            e = BossMonster(edef["name"], hp=edef.get("hp", 500), attack=edef.get("attack", 25), defense=edef.get("defense", 15), **kwargs)
        else:
            e = NPC(edef["name"], hp=edef.get("hp", 50), attack=edef.get("attack", 5), defense=edef.get("defense", 3))
        entities.append(e)
    return entities


def run_demo():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = load_config(os.path.join(project_root, "config", "engine.toml"))
    content_dir = os.path.join(project_root, "content")
    output_dir = os.path.join(project_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    content = load_content(content_dir)
    entities = create_entities_from_content(content)

    if not entities:
        print("No entities loaded from content. Using defaults.")
        entities = [
            Player("Hero", hp=150, attack=12, defense=8),
            NPC("Guard", hp=80, attack=6, defense=4, patrol_route=["gate", "market"]),
            Monster("Goblin", hp=40, attack=8, defense=2, resistance=0.1),
            BossMonster("Dragon", hp=500, attack=25, defense=15, resistance=0.3, shield=50),
        ]

    entity_map = {e.name: e for e in entities}

    dispatcher = EventDispatcher()
    combat = CombatSystem(dispatcher, config)
    interaction = InteractionSystem()

    print("=== Game Engine Demo ===")
    print(f"Loaded {len(entities)} entities: {[e.name for e in entities]}")

    encounters = content.get("encounters", {}).get("encounters", [])
    if not encounters:
        encounters = [
            {"attacker": "Hero", "defender": "Goblin", "elemental_modifier": 1.0},
            {"attacker": "Hero", "defender": "Dragon", "elemental_modifier": 1.2},
            {"attacker": "Goblin", "defender": "Hero", "elemental_modifier": 1.0},
            {"attacker": "Dragon", "defender": "Hero", "elemental_modifier": 1.5},
        ]

    print("\n--- Combat Phase ---")
    for enc in encounters:
        attacker = entity_map.get(enc.get("attacker"))
        defender = entity_map.get(enc.get("defender"))
        if attacker and defender and attacker.alive and defender.alive:
            modifier = enc.get("elemental_modifier", 1.0)
            result = combat.resolve_attack(attacker, defender, elemental_modifier=modifier)
            print(f"  {result['attacker']} attacks {result['defender']}: {result['final_damage']:.1f} damage "
                  f"(HP: {result['defender_hp_before']:.1f} -> {result['defender_hp_after']:.1f})")

    print("\n--- Interaction Phase ---")
    for entity in entities:
        for other in entities:
            if entity is not other and entity.alive and other.alive:
                try:
                    result = interaction.process_interaction(entity, other, "talk")
                except TypeError as e:
                    print(f"  Interaction error between {entity.name} and {other.name}: {e}")
                    break

    print("\n--- Event Log ---")
    event_log = dispatcher.get_event_log()
    print(f"  Total events dispatched: {len(event_log)}")
    for ev in event_log:
        print(f"  [{ev['type']}] {ev['source']} -> {ev['target']} (handled={ev['handled']})")

    combat.save_combat_log(output_dir)
    print(f"\nCombat log saved to {output_dir}/combat_log.json")

    summary = {
        "entities": [e.get_info() for e in entities],
        "combat_log_entries": len(combat.get_combat_log()),
        "events_dispatched": len(event_log),
        "content_loaded": list(content.keys()),
    }
    with open(os.path.join(output_dir, "demo_summary.json"), "w") as f:
        json.dump(summary, f, indent=2)

    print("Demo complete.")
    return summary


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_demo()
