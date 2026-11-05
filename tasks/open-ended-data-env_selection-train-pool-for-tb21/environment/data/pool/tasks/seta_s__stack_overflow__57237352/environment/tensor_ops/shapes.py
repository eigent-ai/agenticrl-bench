import torch

def squeeze_batch(x: torch.Tensor) -> torch.Tensor:
    """Remove the batch dimension (dim 0) if it is size 1."""
    return x.squeeze(1)
