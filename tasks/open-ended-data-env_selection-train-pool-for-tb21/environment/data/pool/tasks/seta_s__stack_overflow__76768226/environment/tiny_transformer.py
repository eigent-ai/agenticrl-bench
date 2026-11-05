import torch
import torch.nn as nn

VOCAB = 256
DIM = 32
N_LAYERS = 2


class SelfAttention(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.q_linear = nn.Linear(dim, dim, bias=False)
        self.k_linear = nn.Linear(dim, dim, bias=False)
        self.v_linear = nn.Linear(dim, dim, bias=False)
        self.out_linear = nn.Linear(dim, dim, bias=False)

    def forward(self, x):
        q = self.q_linear(x)
        k = self.k_linear(x)
        v = self.v_linear(x)
        scale = x.size(-1) ** 0.5
        scores = torch.softmax(q @ k.transpose(-2, -1) / scale, dim=-1)
        return self.out_linear(scores @ v)


class FeedForward(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.fc1 = nn.Linear(dim, dim * 4, bias=False)
        self.fc2 = nn.Linear(dim * 4, dim, bias=False)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


class TransformerBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.attn = SelfAttention(dim)
        self.ffn = FeedForward(dim)
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)

    def forward(self, x):
        x = x + self.attn(self.norm1(x))
        x = x + self.ffn(self.norm2(x))
        return x


class TinyTransformer(nn.Module):
    def __init__(self, vocab=VOCAB, dim=DIM, n_layers=N_LAYERS):
        super().__init__()
        self.embedding = nn.Embedding(vocab, dim)
        self.layers = nn.ModuleList([TransformerBlock(dim) for _ in range(n_layers)])
        self.norm = nn.LayerNorm(dim)
        self.head = nn.Linear(dim, vocab, bias=False)

    def forward(self, input_ids):
        x = self.embedding(input_ids)
        for layer in self.layers:
            x = layer(x)
        x = self.norm(x)
        return self.head(x)
