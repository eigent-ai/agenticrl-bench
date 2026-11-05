import pandas as pd
import numpy as np


def scale_features(input_path, output_path):
    df = pd.read_csv(input_path)
    values = df.values
    mean = np.mean(values, axis=0)
    std = np.std(values, axis=0)
    scaled = (values - mean) / std
    result = pd.DataFrame(scaled, columns=df.columns)
    result.to_csv(output_path, index=False)
    return result
