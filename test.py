import pyaudio
import numpy as np

if __name__ == "__main__":
  factor = 64
  
  p = pyaudio.PyAudio()
  out = p.open(rate=factor*1000, channels=1, format=pyaudio.paInt8, output=True)

  scale = 40

  while True:
    signal = np.array([1 for i in range(factor*1)]+[0 for i in range(factor*1)], dtype=np.int8).flatten()*scale

    out.write(signal)
