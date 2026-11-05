import torch
import torch.nn as nn
from model import SimpleMLP
from data_utils import get_train_data


def main():
    torch.manual_seed(42)

    model = SimpleMLP()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.01)

    train_loader = get_train_data(batch_size=32)

    model.train()
    for epoch in range(50):
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()

    model.eval()
    torch.save(model.state_dict(), "weights/model.pt")
    print(f"Weights saved to weights/model.pt")


if __name__ == "__main__":
    main()
