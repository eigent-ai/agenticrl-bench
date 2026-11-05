import torch
import torch.nn as nn


class ResBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, 3, padding=1, bias=False)
        self.conv2 = nn.Conv2d(channels, channels, 3, padding=1, bias=False)
        self.conv3 = nn.Conv2d(channels, channels, 1, bias=False)
        self.bn = nn.BatchNorm2d(channels)
        self.relu = nn.ReLU(inplace=True)
        self.drop = nn.Dropout(p=0.5)

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn(out)
        out = self.relu(out)
        out = self.drop(out)
        out = self.conv2(out)
        out = self.bn(out)
        out = self.relu(out)
        out = self.conv3(out)
        out = self.bn(out)
        out += residual
        return self.relu(out)


class SimpleNet(nn.Module):
    def __init__(self, in_channels=1, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels, 16, 3, padding=1, bias=False),
            nn.BatchNorm2d(16),
            nn.ReLU(),
        )
        self.res = ResBlock(16)
        self.pool = nn.AdaptiveAvgPool2d(1)
        self.classifier = nn.Linear(16, num_classes)

    def forward(self, x):
        x = self.features(x)
        x = self.res(x)
        x = self.pool(x)
        x = x.flatten(1)
        return self.classifier(x)
