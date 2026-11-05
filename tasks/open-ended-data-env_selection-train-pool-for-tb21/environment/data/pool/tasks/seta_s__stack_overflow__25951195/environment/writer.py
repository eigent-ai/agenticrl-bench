import json
import logging
import os


logger = logging.getLogger("pipeline.writer")
logger.setLevel(logging.CRITICAL)


def write_output(data, output_path):
    try:
        logger.debug("Preparing to write output")
        output_dir = os.path.dirname(output_path)
        os.makedirs(output_dir, exist_ok=True)

        logger.debug("Writing results to %s", output_path)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        file_size = os.path.getsize(output_path)
        logger.debug("Output written successfully: %d bytes", file_size)
        return True

    except Exception as e:
        logger.error("Failed to write output: %s", str(e))
        return False
