"""Main application entry point."""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Utils import helper_func


def process_data(input_data):
    """Process input data through the utility pipeline."""
    result = helper_func(input_data)
    return result


def main():
    """Run the main application logic."""
    data = "project_payload_v2"
    output = process_data(data)
    print(f"Processing complete: {output}")
    return output


if __name__ == "__main__":
    main()
