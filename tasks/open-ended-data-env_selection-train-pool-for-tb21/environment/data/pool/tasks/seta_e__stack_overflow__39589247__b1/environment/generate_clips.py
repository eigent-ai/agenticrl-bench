import wave
import numpy as np

SAMPLE_RATE = 44100
DURATION = 1.0
NFRAMES = int(SAMPLE_RATE * DURATION)

for i in range(10):
    left_val = np.int16(10000 + i * 200)
    right_val = np.int16(5000 + i * 200)
    left = np.full(NFRAMES, left_val, dtype='<i2')
    right = np.full(NFRAMES, right_val, dtype='<i2')
    stereo = np.column_stack([left, right])

    with wave.open(f"clips/clip_{i:03d}.wav", 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(stereo.astype('<i2').tobytes())

print("Generated 10 clips")
