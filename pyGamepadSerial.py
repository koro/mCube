# this works with my gamepad, the indices and directions maybe have to be adapted

import pygame
import sys
import time
import serial
from matplotlib import pyplot as plt

if __name__ == "__main__":
  pygame.init()
  pygame.display.set_mode((400, 400), 0, 8)
  gp = pygame.joystick.Joystick(0)
  gp.init()
  outSerial = serial.Serial("/dev/ttyUSB0", 115200)
  roll = 0.0
  pitch = 0.0
  yaw = 0.0
  thrust = 0.0
#  plt.ion()
  while True:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        msg = mavlink.MAVLink_huch_ext_ctrl_message(1, 1, 0, 0, 0, 0, 0)
        mavL.send(msg)
        sys.exit()
    for i in range(gp.get_numaxes()):
      value = gp.get_axis(i)
      if i == 3:
        roll = -value
      if i == 4:
        pitch = -value
      if i == 2:
        yaw = -value
      if i == 1:
        thrust = -value
#    plt.clf()
#    plt.plot(roll, pitch, "r*")
#    plt.plot(yaw, thrust, "b*")
#    plt.gca().set_xlim((-1.2, 1.2))
#    plt.gca().set_ylim((-1.2, 1.2))
#    plt.draw()
    outString = str(int(127+roll*127))+" "+str(int(127+pitch*127))+" "+str(int(127+yaw*127))+" "+str(int(127+thrust*127))+"\n"
    print outString
    outSerial.write(outString)
    time.sleep(1e-1)
