# implement two synchronous 9600 bit/s UART over stereo sound using 16bit datawords
# reads input data from a gamepad
import pyaudio
import pygame
import random
import sys
import numpy as np
from bitstring import BitArray

binary8 = lambda x: [int(i) for i in BitArray(int=int(x), length=8).bin]

def resample(samples, factor):
  temp = [[sample for i in range(factor)] for sample in samples]
  return np.array(temp).flatten().tolist()

class MagicCube:
  def __init__(self):
    self.factor = 4
    self.scale = 40
    self.p = pyaudio.PyAudio()
    self.out = p.open(rate=9614*factor, channels=2, format=pyaudio.paInt8, output=True) # 104 us for 9600 bits/s
  def binary8(self, x):
    return [int(i) for i in BitArray(int=int(x), length=8).bin]
  def resample(self, samples, factor):
    temp = [[sample for i in range(factor)] for sample in samples]
    return np.array(temp).flatten().tolist()
  def init(self):
    for i in range(20):
      msg = [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1]
      msg.extend([0 for i in range(21)])
      msg = self.resample(msg, factor)
      self.out.write(np.array(zip(msg, msg), dtype=np.int8).flatten()*scale)
  def control(self, pitch, roll, yaw, thrust):
    left = []
    right = []

    left.extend([1, 0])
    right.extend([1, 0])
    
    left.extend(self.binary8(pitch))
    left.extend(self.binary8(thrust))
    right.extend(self.binary8(roll))
    right.extend(self.binary8(yaw))
    
    left.extend([0, 0, 1])
    right.extend([0, 0, 1])
    left.extend([0 for i in range(30)])
    right.extend([0 for i in range(30)])

    left = resample(left, factor)
    right = resample(right, factor)
    signal = np.array(zip(left, right), dtype=np.int8).flatten()*scale

    self.out.write(signal)

if __name__ == "__main__":
  pygame.init()
  pygame.display.set_mode((400, 400), 0, 8)
  gp = pygame.joystick.Joystick(0)
  gp.init()
  
  factor = 4
  scale = 40

  p = pyaudio.PyAudio()
  out = p.open(rate=9614*factor, channels=2, format=pyaudio.paInt8, output=True) # 104 us for 9600 bits/s

  for i in range(20):
    init = [1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1]
    init.extend([0 for i in range(21)])
    init = resample(init, factor)
    out.write(np.array(zip(init, init), dtype=np.int8).flatten()*scale)
 
  roll = 0.0
  pitch = 0.0
  yaw = 0.0
  thrust = 0.0
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
    for i in range(gp.get_numaxes()):
      value = gp.get_axis(i)
      if i == 4:
        pitch = value
      if i == 3:
        roll = value
      if i == 2:
        yaw = value
      if i == 1:
        thrust = value
    left = []
    right = []

    left.extend([1, 0])
    right.extend([1, 0])

    left.extend(binary8(pitch*127))
    left.extend(binary8(thrust*127))

    right.extend(binary8(roll*127))
    right.extend(binary8(yaw*127))
    
    left.extend([0, 0, 1])
    right.extend([0, 0, 1])

    left.extend([0 for i in range(30)])
    right.extend([0 for i in range(30)])

    left = resample(left, factor)
    right = resample(right, factor)

    signal = np.array(zip(left, right), dtype=np.int8).flatten()*scale
    out.write(signal)
