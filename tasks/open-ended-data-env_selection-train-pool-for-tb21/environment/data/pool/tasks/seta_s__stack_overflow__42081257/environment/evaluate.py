import numpy as np
import yaml
import json
import os
from metrics.accuracy import compute_accuracy
from metrics.losses import compute_loss


def load_config(config_path):
    with open(config_path) as f:
        return yaml.safe_load(f)


def evaluate_model(config_path, base_dir):
    config = load_config(config_path)
    data_dir = os.path.join(base_dir, config['data_dir'])

    predictions = np.load(os.path.join(data_dir, 'predictions.npy'))
    labels = np.load(os.path.join(data_dir, 'labels.npy'))

    num_classes = config.get('num_classes', None)
    loss_type = config['loss']

    if num_classes is not None and len(predictions.shape) > 1 and predictions.shape[-1] > num_classes:
        predictions = predictions[:, :num_classes]
        labels = labels[:, :num_classes]

    accuracy = compute_accuracy(predictions, labels, loss_type)
    loss = compute_loss(predictions, labels, loss_type)

    return {
        'accuracy': round(float(accuracy), 6),
        'loss': round(float(loss), 6)
    }


def main():
    base_dir = '/opt/ml-eval-pipeline'
    results = {}

    results['multiclass'] = evaluate_model(
        os.path.join(base_dir, 'configs', 'multiclass.yaml'),
        base_dir
    )

    results['binary'] = evaluate_model(
        os.path.join(base_dir, 'configs', 'binary.yaml'),
        base_dir
    )

    report_dir = os.path.join(base_dir, 'reports')
    os.makedirs(report_dir, exist_ok=True)

    output_path = os.path.join(report_dir, 'results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print("Results written to {}".format(output_path))
    for model, metrics in results.items():
        print("  {}: accuracy={}, loss={}".format(model, metrics['accuracy'], metrics['loss']))


if __name__ == '__main__':
    main()
