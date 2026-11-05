import numpy as np
import torch


def apply_transforms(features, config):
    """Apply configured transformations to feature tensor."""
    transformed = features

    if config.get("normalize", False):
        mean = transformed.mean(dim=0)
        std = transformed.std(dim=0)
        std[std == 0] = 1.0
        transformed = (transformed - mean) / std

    if "scale_factor" in config:
        scale = config["scale_factor"]
        arr = transformed.numpy()
        scale_matrix = np.eye(arr.shape[1]) * scale
        arr = np.matmul(arr, scale_matrix)
        transformed = torch.from_numpy(arr)

    return transformed
