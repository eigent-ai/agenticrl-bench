import argparse
import logging
import sys
import os

from pipeline.logging_config import setup_logging
from pipeline.reader import read_csv
from pipeline.transformer import transform_data
from pipeline.writer import write_output


logger = logging.getLogger("pipeline.main")


def main():
    parser = argparse.ArgumentParser(description="Data Processing Pipeline")
    parser.add_argument("--input", required=True, help="Path to input CSV file")
    parser.add_argument("--output-dir", default="/opt/pipeline/output",
                        help="Output directory for results")
    args = parser.parse_args()

    setup_logging()

    logger.info("Pipeline starting")
    logger.debug("Input file: %s", args.input)
    logger.debug("Output directory: %s", args.output_dir)

    if not os.path.exists(args.input):
        logger.error("Input file not found: %s", args.input)
        return 1

    logger.info("Reading input data")
    data = read_csv(args.input)
    if data is None:
        logger.error("Failed to read input data")
        return 1

    logger.info("Transforming data")
    result = transform_data(data)
    if result is None:
        logger.error("Failed to transform data")
        return 1

    logger.info("Writing output")
    output_path = os.path.join(args.output_dir, "result.json")
    success = write_output(result, output_path)
    if not success:
        logger.error("Failed to write output")
        return 1

    logger.warning("Pipeline completed successfully with %d records processed", len(data))
    return 0


if __name__ == "__main__":
    sys.exit(main())
