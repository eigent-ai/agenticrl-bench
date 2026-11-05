import json
import logging
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from montecarlo.engine import SimulationEngine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def main():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
    with open(config_path) as f:
        config = json.load(f)

    logger.info("Creating simulation engine from config...")
    engine = SimulationEngine.from_config(config)
    logger.info(f"Engine created: {engine}")

    logger.info("Running simulation...")
    samples, stats = engine.run()

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)

    report_path = os.path.join(output_dir, "report.json")
    with open(report_path, "w") as f:
        json.dump(stats, f, indent=2)

    logger.info(f"Report written to {report_path}")
    logger.info(f"Overall status: {stats['status']}")

    return 0 if stats["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
