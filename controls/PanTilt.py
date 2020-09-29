import time
import sys
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

def tilt_up():
  for i in range(0, 40, 2):
    kit.servo[0].angle = i
    time.sleep(0.01)

def pan_clockwise():
  for i in range(0, 180, 2):
    kit.servo[1].angle = i
    time.sleep(0.01)

def tilt_down():
  for i in reversed(range(0, 40, 2)):
    kit.servo[0].angle = i
    time.sleep(0.01)

def pan_counter():
  for i in reversed(range(0, 180, 2)):
    kit.servo[1].angle = i
    time.sleep(0.01)

kit.servo[0].angle = 0
kit.servo[1].angle = 0

while(True):
  pan_clockwise()
  tilt_up()
  pan_counter()
  tilt_down()
  

sys.exit()

