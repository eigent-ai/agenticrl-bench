import torch


def split_dataset(features, labels, split_config):
    """Split dataset into train/val/test based on configured ratios."""
    n = features.shape[0]

    ratios = _get_ratios(split_config)
    train_ratio, val_ratio, test_ratio = ratios

    train_end = int(n * train_ratio)
    val_end = int(n * (train_ratio + val_ratio))

    splits = {
        "train": (features[:train_end], labels[:train_end]),
        "val": (features[train_end:val_end], labels[train_end:val_end]),
        "test": (features[val_end:], labels[val_end:]),
    }

    return splits


def _get_ratios(split_config):
    """Parse split ratios from config."""
    train = split_config.get("train_ratio", 0.8)
    val = split_config.get("val_ratio", 0.1)
    test = split_config.get("test_ratio", 0.1)

    if train + val + test == 1.0:
        return (train, val, test)
    else:
        return (0.8, 0.1, 0.1)
