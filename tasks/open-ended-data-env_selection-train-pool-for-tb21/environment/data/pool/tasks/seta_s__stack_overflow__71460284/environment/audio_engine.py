"""Audio synthesis module for game sound effects.

Generates oscillator-based notes with attack-hold-fade envelopes.
"""

import numpy as np

SAMPLE_RATE = 44100


def render_note(freq=440.0, peak_gain=0.5, attack_time=0.05,
                hold_time=0.5, fade_time=0.03):
    """
    Render an oscillator note with an attack-hold-fade gain envelope.

    Args:
        freq:        Oscillator frequency in Hz.
        peak_gain:   Target gain (0.0-1.0) during the hold phase.
        attack_time: Duration of the gain ramp-up in seconds.
        hold_time:   Duration at peak gain in seconds.
        fade_time:   Duration of the gain ramp-down in seconds.

    Returns:
        Tuple of (sample_rate, samples) where samples is a float32 ndarray.
    """
    total_duration = attack_time + hold_time + fade_time + 0.01
    total_samples = int(SAMPLE_RATE * total_duration)
    t = np.linspace(0, total_duration, total_samples, endpoint=False)
    oscillator = np.sin(2 * np.pi * freq * t)

    envelope = build_envelope(total_samples, peak_gain,
                               attack_time, hold_time, fade_time)
    return SAMPLE_RATE, (oscillator * envelope).astype(np.float32)


def build_envelope(total_samples, peak_gain, attack_time, hold_time, fade_time):
    """
    Build an attack-hold-fade gain envelope as a numpy array.

    Args:
        total_samples: Total length of the envelope in samples.
        peak_gain:     Target gain during the hold phase.
        attack_time:   Duration of the attack ramp in seconds.
        hold_time:     Duration of the hold (constant peak) in seconds.
        fade_time:     Duration of the fade-out ramp in seconds.

    Returns:
        Float64 numpy array of gain values, length == total_samples.
    """
    envelope = np.zeros(total_samples, dtype=np.float64)

    attack_end = int(SAMPLE_RATE * attack_time)
    hold_end   = int(SAMPLE_RATE * (attack_time + hold_time))
    fade_end   = int(SAMPLE_RATE * (attack_time + hold_time + fade_time))

    # Attack phase: ramp gain up to peak.
    if attack_end > 0:
        envelope[:attack_end] = np.geomspace(
            peak_gain,
            peak_gain,
            attack_end,
        )

    # Hold and fade phases.
    if fade_end > attack_end:
        envelope[attack_end:fade_end] = np.geomspace(
            peak_gain,
            1e-4,
            fade_end - attack_end,
        )

    # Silence after fade.
    if fade_end < total_samples:
        envelope[fade_end:] = 1e-4

    return envelope
