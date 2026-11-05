Dataset Validation Pipeline
============================
Usage: validate_dataset.sh -d <data_dir> -o <output_file> [-v]

Required files in <data_dir>: config.json, metadata.csv, data.bin, schema.txt

Output format:
  PASS: <filename>   (file present)
  FAIL: <filename>   (file absent)
  Summary: PASS=N FAIL=M
