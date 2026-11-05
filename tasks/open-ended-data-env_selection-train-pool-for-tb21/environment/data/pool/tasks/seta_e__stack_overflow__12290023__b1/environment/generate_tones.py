import wave
import numpy as np
import os

os.makedirs("/opt/audiopipeline/tones", exist_ok=True)

frequencies = [220, 277, 330, 392, 440, 523, 587, 659, 784, 880]
sample_rate = 44100
duration = 1.0

for i, freq in enumerate(frequencies):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    samples = (np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)

    with wave.open(f"/opt/audiopipeline/tones/{i}.wav", "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(samples.tobytes())

print(f"Generated {len(frequencies)} tone files in /opt/audiopipeline/tones/")
