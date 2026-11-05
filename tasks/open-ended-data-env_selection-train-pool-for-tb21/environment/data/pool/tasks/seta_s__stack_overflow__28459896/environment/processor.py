import numpy as np


def apply_calibrations(sensor_data, sensor_types, cal_funcs):
    """Apply calibration functions to sensor data based on sensor types.

    Uses argsort + searchsorted dispatch for efficient vectorized application
    of different calibration functions to different sensor types.
    """
    func_indices = sensor_types
    func_argsort = np.argsort(func_indices)

    func_ranges = list(np.searchsorted(func_indices, range(len(cal_funcs))))
    func_ranges.append(len(sensor_data))

    out = np.ones_like(sensor_data)

    for i in range(len(cal_funcs)):
        start = func_ranges[i]
        end = func_ranges[i + 1]
        indices = func_argsort[start:end]
        if len(indices) > 0:
            out[indices] = cal_funcs[i](sensor_data[indices])

    return out
