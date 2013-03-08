import sys
import numpy as np
import pyaudio
from bitstring import BitArray
from matplotlib import pyplot as plt 

if __name__ == "__main__":
  sampleRate = 96000
  p = pyaudio.PyAudio()
  print p.get_default_input_device_info()
  inStream = p.open(rate=sampleRate, channels=2, format=pyaudio.paInt16, input=True)

  plt.gcf().canvas._tkcanvas.master.geometry("1500x1000") 
  plt.ion()
#  leftTrues = []
#  intervalLen = 0
  while True:
#  for foo in range(10000):
    data = inStream.read(int(5.5e-1*sampleRate))
    samples = np.fromstring(data, dtype=np.int16)
    left = samples[range(1, len(samples), 2)]

    zero = min(left)
    one = max(left)

    leftBinary = [1 if sample > (one-zero)/2.0 else 0 for sample in left]

    trigger1 = 0
    trigger2 = 0
    triggerLen = int(2.0e-3*sampleRate)
    for i in range(len(leftBinary)-triggerLen):
      if sum(leftBinary[i:i+triggerLen]) == 0:
        for j in range(i, len(leftBinary)):
          if leftBinary[j] > 0:
            trigger1 = j
            for k in range(trigger1, len(leftBinary)-triggerLen):
              if sum(leftBinary[k:k+triggerLen]) == 0:
                trigger2 = k
                break
            break
        break

#    for i in range(trigger1-100, trigger2+100):
#      if leftBinary[i] == 1:
#        leftTrues.append(i-(trigger1-100))
#
#    intervalLen = max([intervalLen, trigger2-trigger1+200])

    plt.clf()
    plt.subplot(211)
    plt.plot(left[trigger1-100:trigger2+100], "b-")
    plt.subplot(212)
    plt.plot(leftBinary[trigger1-100:trigger2+100], "b-")
    plt.gca().set_ylim((0, 1.2))
    plt.draw()
#  plt.hist(leftTrues, bins=intervalLen)
#  plt.gca().set_xlim((0, intervalLen))
#  plt.show()
