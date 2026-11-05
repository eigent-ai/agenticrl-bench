import numpy as np
from scipy.signal import lombscargle


def detect_period(times, values):
    """Detect dominant period of irregularly-sampled data using Lomb-Scargle periodogram."""
    freqs = np.linspace(0.01, 0.5, 500)

    pgram = lombscargle(times, values - values.mean(), freqs, normalize=True)

    peak_idx = np.argmax(pgram)
    detected_freq_hz = freqs[peak_idx]
    detected_period = 1.0 / detected_freq_hz

    return {
        "detected_period": float(detected_period),
        "detected_freq": float(detected_freq_hz),
        "peak_power": float(pgram[peak_idx])
    }
