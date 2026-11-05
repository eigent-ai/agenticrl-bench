import torch
import torch.nn as nn
import torch.nn.functional as F


class TwoLayerNet(nn.Module):
    def __init__(self, input_dim=10, hidden_dim=20, output_dim=2):
        super().__init__()
        self.linear1 = nn.Linear(input_dim, hidden_dim)
        self.linear2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        h = F.relu(self.linear1(x))
        return self.linear2(h)
