import json

with open("output/fixed_result.json") as f:
    fixed = json.load(f)
with open("output/split_result.json") as f:
    split = json.load(f)
with open("output/variable_result.json") as f:
    variable = json.load(f)

summary = {
    "total_values_fixed": fixed["total_values"],
    "num_batches_fixed": fixed["num_batches"],
    "total_values_split": split["total_values"],
    "num_parts": split["num_parts"],
    "total_values_variable": variable["total_values"],
    "num_variable_batches": variable["num_batches"],
}

with open("output/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("Pipeline completed successfully.")
