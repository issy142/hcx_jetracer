import dis_4sens
print("hello1")
from jetracer.nvidia_racecar import NvidiaRacecar
print("hello2")
import numpy as np
#import RPi.GPIO as GPIO
import time
print("hello3")
#import dis_4sens
import csv

print("hello")

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
car.steering_gain = 1.0
car.steering_offset = 0.0

rightMax = 1.0
leftMax = -1.0

steerParam = 1.0 # steerParam * facingAngle で facingAngle[rad]曲がる


# throttle setting
car.throttle_gain = 0.5

speedHigh = 10
speedLow = 0.5


# *Distance are the acquired distance to the wall from each sensor
rightFrontDistance = []
rightRearDistance = []


# start time
# startTime = time.time()

print(1)
temp = dis_4sens.readTemp()
print(temp)

# Driving program
try:
    while isLoop:
        print("AAA")
        print(dis_4sens.readSonic(4, temp)) # Right front
        rightFrontDistance.append(dis_4sens.readSonic(1, temp)) # Right front
        rightRearDistance.append(dis_4sens.readSonic(2, temp)) # Right rear

        # Figure out status
        ## distance from car to the wall
        distance = (rightFrontDistance[-1] + rightRearDistance[-1]) / 2
        farFromWall = distance > centerLine + thresWidth / 2
        closeToWall = distance < centerLine - thresWidth / 2

        ## rotaion of the car
        facingAngle = np.arctan((rightFrontDistance[-1] - rightRearDistance[-1]) / betweenSensors)
        # calcurate facing angle #

        print("BBB")
        if farFromWall:
            car.throttle = speedLow
            car.steering = rightMax
            # turning right #
        elif closeToWall:
            car.throttle = speedLow
            car.steering = leftMax
            #  turnning left #
        elif abs(facingAngle) > facingAngleThres:
            car.steering = steerParam * facingAngle
            car.throttle = speedLow
            # turning with appropriate angle #
        else:
            car.steering = 0.0 # keep sttering straight #
            car.throttle = speedHigh # Move Foward #


except KeyboardInterrupt:
    print('stop!')
    car.throttle = 0.0
    car.steering = 0.0
    GPIO.cleanup()
    with open('SpeedHigh_' + str(SppedHigh) + '_SpeedLow_' + str(SpeedLow) + '_Center_' + str(centerLine) + 'Width_' + str(thresWidth) + '.csv') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(timeStamp)
        writer.writerow(rightFrontDistance)
        writer.writerow(rightRearDistance)

print('end')