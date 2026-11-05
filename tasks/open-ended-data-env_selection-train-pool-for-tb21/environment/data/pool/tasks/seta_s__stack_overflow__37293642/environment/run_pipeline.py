import json
import os

from config import CONFIG
from callbacks import EarlyStoppingByLossVal, MetricsLogger, CheckpointSaver
from trainer import Trainer
from analyze_metrics import analyze


def main():
    os.makedirs('output', exist_ok=True)
    os.makedirs(CONFIG.get('checkpoint_dir', 'output/checkpoints'), exist_ok=True)

    for f in [CONFIG['metrics_file'], CONFIG['report_file']]:
        if os.path.exists(f):
            os.unlink(f)

    early_stop = EarlyStoppingByLossVal(
        monitor=CONFIG['monitor'],
        value=CONFIG['early_stop_threshold'],
        verbose=CONFIG.get('verbose', 0),
    )
    metrics_logger = MetricsLogger(CONFIG['metrics_file'])
    checkpoint_saver = CheckpointSaver(CONFIG['checkpoint_dir'])

    callbacks = [early_stop, checkpoint_saver, metrics_logger]
    trainer = Trainer(callbacks=callbacks, max_epochs=CONFIG['max_epochs'])

    print("Starting training...")
    history = trainer.train()
    print(f"Training complete. {len(history)} epochs.")

    print("Analyzing metrics...")
    report = analyze(
        CONFIG['metrics_file'],
        min_thresh=CONFIG['filter_min'],
        max_thresh=CONFIG['filter_max'],
    )

    with open(CONFIG['report_file'], 'w') as f:
        json.dump(report, f, indent=2)
    print(f"Report saved to {CONFIG['report_file']}")


if __name__ == '__main__':
    main()
