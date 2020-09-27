from jetracer.nvidia_racecar import NvidiaRacecar

print("Hello")
# steering setting
car = NvidiaRacecar()
print("good morning")
car.steering_gain = 1.0
car.steering_offset = 0.0


# throttle setting
car.throttle_gain = 0.5

speedHigh = 10
speedLow = 0.5

farFromWall = True

# Driving program
try:
    while True:
        print("konnnichiwa")
       
        if farFromWall:
            car.throttle = 10
            car.steering = 1
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