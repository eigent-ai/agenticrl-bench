import numpy as np


def load_sensor_data(filepath):
    """Load sensor readings from a CSV file.

    Returns a 1-D numpy array of sensor values.
    """
    data = np.loadtxt(filepath, delimiter=',', skiprows=1)
    return data
