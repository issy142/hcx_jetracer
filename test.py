import dis_full_maki
#from jetracer.nvidia_racecar import NvidiaRacecar

#car = NvidiaRacecar()
#car.throttle_gain = 0.0
#car.throttle = 0.0
#tempareture
temp = dis_full_maki.readTemp()
#print(temp)
#sensor1
dis = dis_full_maki.readSonic(4,temp)
for i in range(4):
    i += 1
    dis = dis_full_maki.readSonic(i,temp)
    print(dis)