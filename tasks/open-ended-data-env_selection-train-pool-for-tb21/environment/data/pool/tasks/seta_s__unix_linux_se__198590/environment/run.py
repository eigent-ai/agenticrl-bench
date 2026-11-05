import configparser
import os
import sys

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config', 'pipeline.ini'))

input_dir = config.get('pipeline', 'input_dir')
output_dir = config.get('pipeline', 'output_dir')
temp_dir = config.get('pipeline', 'temp_dir')

os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

input_file = os.path.join(input_dir, 'input.txt')
if not os.path.exists(input_file):
    print(f"ERROR: Input file not found: {input_file}", file=sys.stderr)
    sys.exit(1)

with open(input_file) as f:
    data = f.read()

# Stage 1: number each line
lines = data.strip().split('\n')
numbered = []
for i, line in enumerate(lines, 1):
    numbered.append(f"{i}: {line}")
stage1_output = '\n'.join(numbered) + '\n'

with open(os.path.join(temp_dir, 'stage1_out.txt'), 'w') as f:
    f.write(stage1_output)

print("Stage 1 complete.")
