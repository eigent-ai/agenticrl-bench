#!/usr/bin/env python3
"""Main pipeline entry point for experimental data analysis."""

import os
import yaml
from src.data_loader import load_dataset
from src.report_generator import generate_report
from src.plotter import create_summary_plot


def main():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    pipeline_config = config["pipeline"]
    output_dir = pipeline_config["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    datasets = {}
    for name, ds_config in config["datasets"].items():
        data, n_rows = load_dataset(ds_config["file"], ds_config["columns"])
        datasets[name] = {
            "data": data,
            "n_rows": n_rows,
            "config": ds_config,
        }

    report_path = os.path.join(output_dir, pipeline_config["report_file"])
    generate_report(datasets, report_path, config)

    plot_path = os.path.join(output_dir, pipeline_config["plot_file"])
    create_summary_plot(datasets, plot_path, config)

    print(f"Pipeline complete. Output written to {output_dir}/")


if __name__ == "__main__":
    main()
