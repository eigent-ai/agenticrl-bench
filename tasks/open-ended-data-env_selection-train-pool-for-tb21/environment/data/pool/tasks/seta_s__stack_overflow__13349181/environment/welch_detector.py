import numpy as np
from scipy.signal import welch as scipy_welch
from scipy.fft import fft, fftfreq
from .utils import find_peak_power


def detect_and_compare(times, values):
    """Compare Welch PSD estimate with manual periodogram for power scaling validation."""
    dt = times[1] - times[0]
    fs = 1.0 / dt

    freqs_welch, psd_welch = scipy_welch(values, fs=fs, nperseg=256)

    N = len(values)
    fft_vals = fft(values)
    freqs_manual = fftfreq(N, d=dt)[:N // 2]
    power_manual = 2.0 * np.abs(fft_vals[:N // 2]) ** 2 / N ** 2

    welch_power, welch_freq = find_peak_power(freqs_welch, psd_welch)
    manual_power, manual_freq = find_peak_power(np.abs(freqs_manual), power_manual)

    detected_period = 1.0 / welch_freq if welch_freq > 0 else float('inf')

    return {
        "detected_period": detected_period,
        "welch_power": welch_power,
        "manual_power": manual_power,
        "welch_peak_freq": welch_freq,
        "manual_peak_freq": manual_freq,
    }
