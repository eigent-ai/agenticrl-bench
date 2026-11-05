#!/usr/bin/env python3
"""Game engine simulation runner.

Usage:
    python run_simulation.py --scenario chase
    python run_simulation.py --scenario slopes
    python run_simulation.py --scenario combat
    python run_simulation.py --scenario stress
    python run_simulation.py --all
"""

import argparse
import json
import logging
import os
import sys

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "simulation.log")

SCENARIO_MAP = {
    "chase":  "scenarios.chase.ChaseScenario",
    "slopes": "scenarios.slopes.SlopesScenario",
    "combat": "scenarios.combat.CombatScenario",
    "stress": "scenarios.stress.StressScenario",
}


def _load_physics_config():
    cfg_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "config", "physics.json"
    )
    if os.path.exists(cfg_path):
        with open(cfg_path) as f:
            return json.load(f)
    return {}


def _import_scenario(dotted_path):
    module_path, class_name = dotted_path.rsplit(".", 1)
    mod = __import__(module_path, fromlist=[class_name])
    return getattr(mod, class_name)


def _setup_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)

    fh = logging.FileHandler(LOG_FILE)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(name)s] %(levelname)s: %(message)s"
    ))
    root.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    root.addHandler(sh)


def run_scenario(name, physics_config):
    if name not in SCENARIO_MAP:
        print(f"Unknown scenario: {name}", file=sys.stderr)
        return None

    cls = _import_scenario(SCENARIO_MAP[name])
    scenario = cls(physics_config)
    result = scenario.run()
    return result


def main():
    parser = argparse.ArgumentParser(description="Run game simulation scenarios")
    parser.add_argument("--scenario", type=str, help="Run a single scenario by name")
    parser.add_argument("--all", action="store_true", help="Run all scenarios")
    args = parser.parse_args()

    if not args.scenario and not args.all:
        parser.print_help()
        sys.exit(1)

    _setup_logging()
    logger = logging.getLogger("main")
    physics_config = _load_physics_config()

    if args.scenario:
        scenarios_to_run = [args.scenario]
    else:
        scenarios_to_run = list(SCENARIO_MAP.keys())

    results = {}
    all_passed = True

    for name in scenarios_to_run:
        logger.info("=" * 60)
        logger.info("Running scenario: %s", name)
        logger.info("=" * 60)

        try:
            result = run_scenario(name, physics_config)
            if result is None:
                all_passed = False
                results[name] = {"passed": False, "error": "Unknown scenario"}
                continue
            results[name] = {
                "passed": result.passed,
                "details": result.details,
                "errors": result.errors,
            }
            status = "PASSED" if result.passed else "FAILED"
            print(f"Scenario '{name}': {status}")
            if not result.passed:
                all_passed = False
                for err in result.errors:
                    print(f"  - {err}")
        except Exception as exc:
            all_passed = False
            results[name] = {"passed": False, "error": str(exc)}
            print(f"Scenario '{name}': CRASHED — {exc}")
            logger.exception("Scenario %s crashed", name)

    print()
    if args.all:
        if all_passed:
            print("All scenarios passed")
        else:
            failed = [n for n, r in results.items() if not r["passed"]]
            print(f"FAILED scenarios: {', '.join(failed)}")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
