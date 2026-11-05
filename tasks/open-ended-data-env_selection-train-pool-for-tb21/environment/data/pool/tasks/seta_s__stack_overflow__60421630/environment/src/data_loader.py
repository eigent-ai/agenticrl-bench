import pandas as pd
import torch
import numpy as np


def load_dataset(csv_path):
    """Load CSV dataset and return feature tensor and label tensor."""
    df = pd.read_csv(csv_path)

    label_col = "label"
    feature_cols = [c for c in df.columns if c != label_col]

    features = torch.tensor(df[feature_cols].values, dtype=torch.float32)
    labels = torch.tensor(df[label_col].values, dtype=torch.long)

    return features, labels
