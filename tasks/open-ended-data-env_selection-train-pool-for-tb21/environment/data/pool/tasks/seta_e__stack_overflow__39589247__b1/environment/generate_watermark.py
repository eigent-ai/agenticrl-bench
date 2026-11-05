import wave
import numpy as np

SAMPLE_RATE = 44100
DURATION = 0.2
NFRAMES = int(SAMPLE_RATE * DURATION)  # 8820 samples

val = np.int16(2000)
left = np.full(NFRAMES, val, dtype='<i2')
right = np.full(NFRAMES, val, dtype='<i2')
stereo = np.column_stack([left, right])

with wave.open("watermark.wav", 'wb') as wf:
    wf.setnchannels(2)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(stereo.astype('<i2').tobytes())

print("Generated watermark")
