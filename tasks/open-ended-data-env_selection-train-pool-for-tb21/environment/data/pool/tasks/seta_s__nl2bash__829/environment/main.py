#!/usr/bin/env python3
"""Main application entry point for project-alpha."""

import sys
import os
import logging

logger = logging.getLogger(__name__)


def load_config():
    """Load application configuration from environment."""
    config = {
        "data_dir": os.environ.get("DATA_DIR", os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data"
        )),
        "log_level": os.environ.get("LOG_LEVEL", "INFO"),
        "max_retries": int(os.environ.get("MAX_RETRIES", "3")),
        "batch_size": int(os.environ.get("BATCH_SIZE", "100")),
    }
    return config


def process_batch(items, batch_size=100):
    """Process items in batches."""
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        processed = [transform(item) for item in batch]
        results.extend(processed)
        logger.info("Processed batch %d/%d", i // batch_size + 1,
                     (len(items) + batch_size - 1) // batch_size)
    return results


def transform(item):
    """Apply transformation to a single data item."""
    if isinstance(item, dict):
        return {k: v.strip() if isinstance(v, str) else v
                for k, v in item.items()}
    return item


def validate_data_directory(data_dir):
    """Ensure the data directory exists and is accessible."""
    if not os.path.isdir(data_dir):
        logger.error("Data directory not found: %s", data_dir)
        return False
    required_files = ["dataset.db"]
    for fname in required_files:
        fpath = os.path.join(data_dir, fname)
        if not os.path.isfile(fpath):
            logger.warning("Expected file missing: %s", fpath)
    return True


def main():
    """Run the main application pipeline."""
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    config = load_config()
    logger.info("Application starting with config: %s", config)

    data_dir = config["data_dir"]
    if not validate_data_directory(data_dir):
        logger.error("Cannot proceed without valid data directory")
        return 1

    logger.info("Data directory validated: %s", data_dir)
    logger.info("Application ready.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
