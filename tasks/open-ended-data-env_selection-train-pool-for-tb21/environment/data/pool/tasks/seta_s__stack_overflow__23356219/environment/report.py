"""Summary report generation."""
import json
import numpy as np


def generate_summary_report(signal_count, all_times, all_values,
                            heatmap_result, spatial_result,
                            bins, grid_size, output_path):
    """Generate a JSON summary report of pipeline results.

    Args:
        signal_count: number of signals processed
        all_times: list of all time values
        all_values: list of all signal values
        heatmap_result: dict from heatmap generation
        spatial_result: dict from spatial map generation
        bins: bin count used for heatmap
        grid_size: grid size used for spatial interpolation
        output_path: path to write JSON report
    """
    report = {
        "signal_count": signal_count,
        "total_data_points": len(all_times),
        "min_time": heatmap_result["t_min"],
        "max_time": heatmap_result["t_max"],
        "min_value": heatmap_result["v_min"],
        "max_value": heatmap_result["v_max"],
        "bins": bins,
        "heatmap_shape": heatmap_result["heatmap_shape"],
        "spatial_grid_size": bins,
        "spatial_temp_range": [
            spatial_result["temp_min"],
            spatial_result["temp_max"],
        ],
    }

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return report
