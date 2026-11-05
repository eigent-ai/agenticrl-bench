"""Top-level driver: run all three pipeline stages in order."""
import os, sys

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')

def setup():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    setup()
    print('[1/3] Merging logs...')
    from merger import merge_logs
    merge_logs()
    print('[2/3] Annotating names...')
    from annotator import annotate_names
    annotate_names()
    print('[3/3] Batch processing...')
    from batch_processor import run
    run()
    print('Pipeline complete.')

if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(__file__))
    main()
