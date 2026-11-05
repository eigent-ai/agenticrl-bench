import torch


def compute_l1_reg(layer, lambda1):
    """Compute L1 regularization penalty for a linear layer's weights."""
    return lambda1 * torch.norm(layer.weight.data, p=1)
