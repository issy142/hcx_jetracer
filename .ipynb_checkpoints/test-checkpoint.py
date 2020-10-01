import dis_4sens
import RPi.GPIO as GPIO
#from jetracer.nvidia_racecar import NvidiaRacecar

#car = NvidiaRacecar()
#car.throttle_gain = 0.0
#car.throttle = 0.0
#tempareture
temp = dis_4sens.readTemp()
print(temp)

for i in range(2):
    i += 1
    dis = dis_4sens.readSonic(i,temp)
    print(dis)
