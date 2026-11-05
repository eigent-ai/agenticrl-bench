import re


class LogParser:
    def __init__(self):
        self.epoch_pattern = re.compile(r"Epoch (\d+)/(\d+)")
        self.loss_pattern = re.compile(r"loss: (\d+\.\d+)")

    def parse(self, filepath):
        entries = []
        current_epoch = None
        total_epochs = None

        with open(filepath, "r") as f:
            for line in f:
                epoch_match = self.epoch_pattern.search(line)
                if epoch_match:
                    current_epoch = int(epoch_match.group(1))
                    total_epochs = int(epoch_match.group(2))
                    continue

                loss_match = self.loss_pattern.search(line)
                if loss_match and current_epoch is not None:
                    entry = {
                        "epoch": current_epoch,
                        "total_epochs": total_epochs,
                        "loss": float(loss_match.group(1)),
                    }
                    entries.append(entry)
                    current_epoch = None

        return entries
