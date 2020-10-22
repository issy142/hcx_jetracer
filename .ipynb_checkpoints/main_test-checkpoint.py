import dis_4sens
#print("hello1")
from jetracer.nvidia_racecar import NvidiaRacecar
#print("hello2")
import numpy as np
#import RPi.GPIO as GPIO
import time
#print("hello3")
#import dis_4sens
import csv

#print("hello")

# parameter setting
# 長さの単位はcm
isLoop = True

centerLine = 30
thresWidth = 15
facingAngleThres = 15
betweenSensors = 20

timeStamp = []
timeStamp.append(time.time())

print("carmachi")
# steering setting
car = NvidiaRacecar()
#car.steering_gain = 1.0
#car.steering_offset = 0.0

rightMax = 1.0
leftMax = -1.0

steerParam = 1.0 # steerParam * facingAngle で facingAngle[rad]曲がる


# throttle setting
#car.throttle_gain = 0.5

speedHigh = 10
speedLow = 0.5


# *Distance are the acquired distance to the wall from each sensor
rightFrontDistance = []
rightRearDistance = []


# start time
# startTime = time.time()

#print(1)
temp = dis_4sens.readTemp()
print("Temperature =", temp)

print(dis_4sens.readSonic(4, temp)) 
print("Amazing!!! YOU ARE GENIUS!!!")
