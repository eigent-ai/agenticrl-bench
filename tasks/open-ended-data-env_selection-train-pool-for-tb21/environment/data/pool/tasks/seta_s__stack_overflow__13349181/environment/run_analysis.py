import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyzer.utils import load_signal
from analyzer.lombscargle_detector import detect_period
from analyzer.welch_detector import detect_and_compare
from analyzer.autocorr_detector import detect_period_samples


def main():
    os.makedirs('results', exist_ok=True)

    with open('ground_truth.json', 'r') as f:
        truth = json.load(f)

    # Lomb-Scargle on signal_sine
    t, v = load_signal('data/signal_sine.csv')
    result_sine = detect_period(t, v)
    result_sine['signal'] = 'signal_sine'
    result_sine['true_period'] = truth['signal_sine']['true_period']
    result_sine['method'] = 'lombscargle'
    with open('results/signal_sine.json', 'w') as f:
        json.dump(result_sine, f, indent=2)
    print(f"signal_sine: detected_period={result_sine['detected_period']:.4f}, true={result_sine['true_period']:.4f}")

    # Lomb-Scargle on signal_fast
    t, v = load_signal('data/signal_fast.csv')
    result_fast = detect_period(t, v)
    result_fast['signal'] = 'signal_fast'
    result_fast['true_period'] = truth['signal_fast']['true_period']
    result_fast['method'] = 'lombscargle'
    with open('results/signal_fast.json', 'w') as f:
        json.dump(result_fast, f, indent=2)
    print(f"signal_fast: detected_period={result_fast['detected_period']:.4f}, true={result_fast['true_period']:.4f}")

    # Lomb-Scargle on signal_harmonic
    t, v = load_signal('data/signal_harmonic.csv')
    result_harm = detect_period(t, v)
    result_harm['signal'] = 'signal_harmonic'
    result_harm['true_period'] = truth['signal_harmonic']['true_period']
    result_harm['method'] = 'lombscargle'
    with open('results/signal_harmonic.json', 'w') as f:
        json.dump(result_harm, f, indent=2)
    print(f"signal_harmonic: detected_period={result_harm['detected_period']:.4f}, true={result_harm['true_period']:.4f}")

    # Autocorrelation on signal_discrete
    t, v = load_signal('data/signal_discrete.csv')
    fs = truth['signal_discrete']['sampling_rate']
    result_disc = detect_period_samples(v, fs)
    result_disc['signal'] = 'signal_discrete'
    result_disc['true_period_samples'] = truth['signal_discrete']['true_period_samples']
    result_disc['true_period_seconds'] = truth['signal_discrete']['true_period_seconds']
    result_disc['method'] = 'autocorrelation'
    with open('results/signal_discrete.json', 'w') as f:
        json.dump(result_disc, f, indent=2)
    print(f"signal_discrete: detected_period_samples={result_disc['detected_period_samples']}, true=5")

    # Welch comparison on signal_sine (regularly sampled)
    t, v = load_signal('data/signal_sine.csv')
    comparison = detect_and_compare(t, v)
    comparison['signal'] = 'signal_sine'
    comparison['method'] = 'welch_vs_manual'
    with open('results/comparison.json', 'w') as f:
        json.dump(comparison, f, indent=2)
    print(f"comparison: welch_power={comparison['welch_power']:.6f}, manual_power={comparison['manual_power']:.6f}")

    print("\nAnalysis complete. Results written to results/")


if __name__ == '__main__':
    main()
