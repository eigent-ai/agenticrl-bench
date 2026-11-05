import json
import torch
import torch.nn as nn
from model import SimpleMLP
from data_utils import get_train_data, get_val_data


def load_config():
    with open("config.json", "r") as f:
        return json.load(f)


def train_model(num_epochs=None, weights_path="weights/model.pt", verbose=True):
    config = load_config()
    torch.manual_seed(config["seed"])

    if num_epochs is None:
        num_epochs = config["epochs"]

    model = SimpleMLP()
    model.load_state_dict(torch.load(weights_path, weights_only=True))

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=config["lr"])

    train_loader = get_train_data(batch_size=config["batch_size"])
    val_loader = get_val_data(batch_size=config["batch_size"])

    model.train()
    train_losses = []
    val_results = []

    for epoch in range(num_epochs):
        running_loss = 0.0
        correct = 0
        total = 0

        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            loss = criterion(outputs, y_batch)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            _, predicted = torch.max(outputs, 1)
            total += y_batch.size(0)
            correct += (predicted == y_batch).sum().item()

        train_loss = running_loss / len(train_loader)
        train_acc = correct / total
        train_losses.append(train_loss)

        if verbose:
            print(f"Epoch {epoch+1}/{num_epochs} - "
                  f"Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.4f}")

        # Validation phase
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        for X_val, y_val in val_loader:
            val_outputs = model(X_val)
            v_loss = criterion(val_outputs, y_val)
            val_loss += v_loss.item()
            _, val_predicted = torch.max(val_outputs, 1)
            val_total += y_val.size(0)
            val_correct += (val_predicted == y_val).sum().item()

        val_loss = val_loss / len(val_loader)
        val_acc = val_correct / val_total
        val_results.append({"loss": val_loss, "accuracy": val_acc})

        if verbose:
            print(f"           Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.4f}")

    return {
        "model": model,
        "train_losses": train_losses,
        "val_results": val_results,
    }


if __name__ == "__main__":
    results = train_model()
    print("\nTraining complete.")
    print(f"Final val accuracy: {results['val_results'][-1]['accuracy']:.4f}")
