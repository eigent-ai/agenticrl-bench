import csv
import json
import os


class Callback:
    """Base class for training callbacks."""
    def on_epoch_end(self, epoch, logs=None):
        pass

    def on_train_end(self, logs=None):
        pass


class EarlyStoppingByLossVal(Callback):
    """Stop training when a monitored metric drops below a threshold."""
    def __init__(self, monitor='val_loss', value=0.5, verbose=0):
        super(Callback, self).__init__()
        self.monitor = monitor
        self.value = value
        self.verbose = verbose

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        current = logs.get(self.monitor)
        if current is None:
            import warnings
            warnings.warn(
                f"Early stopping conditioned on metric `{self.monitor}` "
                f"which is not available. Available metrics are: "
                f"{','.join(logs.keys())}",
                RuntimeWarning,
            )
            return
        if current > self.value:
            if self.verbose > 0:
                print(
                    f"Epoch {epoch}: early stopping threshold reached, "
                    f"{self.monitor}={current:.4f}"
                )
            if hasattr(self, 'trainer'):
                self.trainer.stop_training = True


class MetricsLogger(Callback):
    """Log training metrics to a CSV file each epoch."""
    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self._header_written = False

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        file_exists = os.path.exists(self.filepath)
        with open(self.filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists and not self._header_written:
                writer.writerow(['epoch', 'train_loss', 'val_loss'])
                self._header_written = True
            writer.writerow([epoch, logs.get('train_loss', 0), logs.get('val_loss', 0)])

    def on_train_end(self, logs=None):
        pass


class CheckpointSaver(Callback):
    """Save model checkpoint when monitored metric improves."""
    def __init__(self, dirpath, monitor='val_loss', max_saves=3):
        super().__init__()
        self.dirpath = dirpath
        self.monitor = monitor
        self.max_saves = max_saves
        self.best = float('inf')
        self.save_count = 0
        os.makedirs(dirpath, exist_ok=True)

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        current = logs.get(self.monitor)
        if current is not None and current < self.best:
            self.best = current
            self.save_count += 1
            filepath = os.path.join(
                self.dirpath, f'checkpoint_epoch_{epoch}.json'
            )
            with open(filepath, 'w') as f:
                json.dump({'epoch': epoch, self.monitor: current}, f)
            if self.save_count >= self.max_saves and hasattr(self, 'trainer'):
                self.trainer.callbacks.remove(self)

    def on_train_end(self, logs=None):
        pass
