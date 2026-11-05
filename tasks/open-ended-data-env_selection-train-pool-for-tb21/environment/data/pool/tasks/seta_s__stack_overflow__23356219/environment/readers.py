"""CSV reader for timeseries and spatial sensor data."""
import os
import csv
import numpy as np


def read_timeseries_files(directory):
    """Read all timeseries CSV files from directory.

    Returns:
        all_times: list of all time values
        all_values: list of all sensor values
        signal_count: number of files read
    """
    all_times = []
    all_values = []
    signal_count = 0

    entries = sorted(os.listdir(directory))

    for fname in entries:
        fpath = os.path.join(directory, fname)
        if not os.path.isfile(fpath):
            continue
        signal_count += 1

        times = []
        values = []
        with open(fpath, "r") as f:
            reader = csv.reader(f, delimiter='\t')
            try:
                header = next(reader)
            except StopIteration:
                continue
            for row in reader:
                if len(row) >= 2:
                    times.append(float(row[0]))
                    values.append(float(row[1]))

        all_times.extend(times)
        all_values.extend(values)

    return all_times, all_values, signal_count


def read_spatial_files(directory):
    """Read all spatial CSV files from directory.

    Returns:
        list of dicts with 'x', 'y', 'temperature' arrays
    """
    spatial_data = []

    for fname in sorted(os.listdir(directory)):
        if not fname.endswith(".csv"):
            continue
        fpath = os.path.join(directory, fname)

        x_vals = []
        y_vals = []
        temp_vals = []

        with open(fpath, "r") as f:
            reader = csv.reader(f, delimiter=',')
            header = next(reader)
            for row in reader:
                if len(row) >= 3:
                    x_vals.append(float(row[0]))
                    y_vals.append(float(row[1]))
                    temp_vals.append(float(row[2]))

        spatial_data.append({
            "x": np.array(x_vals),
            "y": np.array(y_vals),
            "temperature": np.array(temp_vals),
        })

    return spatial_data
