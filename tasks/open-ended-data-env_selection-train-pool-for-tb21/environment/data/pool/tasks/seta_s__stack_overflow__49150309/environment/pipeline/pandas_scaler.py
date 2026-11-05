import pandas as pd


def scale_features(input_path, output_path):
    df = pd.read_csv(input_path)
    scaled = (df - df.mean()) / df.std(ddof=0)
    scaled.to_csv(output_path, index=False)
    return scaled
