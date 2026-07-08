from cv2 import mulTransposed
import pyaudio
import numpy as np

CHUNK = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

muted = False

def get_audio_level():

    global muted

    try:
        data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.int16)
    except:
        return 0, muted

    # 🔇 If muted → stop bar
    if muted:
        return 0, True

    # 🔊 Calculate volume
    volume = np.abs(data).mean() / 50

    # 🔥 Prevent very small values (so bar doesn’t look dead)
    if volume < 1:
        volume = 1

    return int(volume), False