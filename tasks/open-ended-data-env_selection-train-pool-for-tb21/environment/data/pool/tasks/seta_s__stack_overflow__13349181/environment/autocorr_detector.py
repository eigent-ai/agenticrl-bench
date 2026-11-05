import numpy as np
from scipy.fft import fft, ifft


def detect_period_samples(values, fs):
    """Detect period in samples using FFT-based autocorrelation."""
    N = len(values)

    fft_vals = fft(values, n=2 * N)
    acf = np.real(ifft(fft_vals * np.conj(fft_vals)))[:N]
    acf = acf / acf[0]

    min_lag = 2
    threshold = 0.5

    valley_found = False
    valley_idx = min_lag
    for i in range(min_lag, N // 2):
        if acf[i] < threshold:
            valley_found = True
            valley_idx = i
            break

    peak_lag = -1
    if valley_found:
        for j in range(valley_idx, N // 2):
            if acf[j] > threshold:
                peak_lag = j
                break

    return {
        "detected_period_samples": int(peak_lag),
        "detected_period_seconds": float(peak_lag / fs) if peak_lag > 0 else -1.0
    }
