#!/usr/bin/env python
# -*- coding: utf-8 -*-
# HC-SR04 ultrasonic range sensor
# with ADT7410 temperature sensor for sonic velocity correction
# ultrasonic
#   GPIO 17 output  = "Trig"
#   GPIO 27 input = "Echo"
 
 
import time
import RPi.GPIO as GPIO
import smbus
import random
import csv
import sys
 
# prepare for ADT7410 temperature sensor 
bus = smbus.SMBus(1)
address_adt7410 = 0x48
register_adt7410 = 0x00

# 保存ファイル名
saveName = "test0921"
 
# prepare for HC-SR04 ultrasonic sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.TEGRA_SOC)
GPIO.setup('UART2_RTS',GPIO.OUT)
GPIO.setup('SPI2_SCK',GPIO.IN)
        
    
 
# detect temperature in C
def read_adt7410():
    word_data =  bus.read_word_data(address_adt7410, register_adt7410)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    data = data>>3 # 13ビットデータ
    if data & 0x1000 == 0:  # 温度が正または0の場合
        #temperature = data*0.0625
        pass
    else: # 温度が負の場合、 絶対値を取ってからマイナスをかける
    #    temperature = ( (~data&0x1fff) + 1)*-0.0625
        pass
    temperature = 20 # ここで温度を指定！
    return temperature
 
 
def reading_sonic(sensor, temp):    
    if sensor == 0:
        GPIO.output('UART2_RTS', GPIO.LOW)
         
        time.sleep(0.3)
        # send a 10us plus to Trigger
        GPIO.output('UART2_RTS', True)
        time.sleep(0.00001)        
        GPIO.output('UART2_RTS', False)
 
        # detect TTL level signal on Echo
        while GPIO.input('SPI2_SCK') == 0:
          signaloff = time.time()
        while GPIO.input('SPI2_SCK') == 1:
          signalon = time.time()
         
        # calculate the time interval
        timepassed = signalon - signaloff
         
        # we now have our distance but it's not in a useful unit of
        # measurement. So now we convert this distance into centimetres
        distance = timepassed * (331.50 + 0.606681 * temp) * 100 / 2
         
        # return the distance of an object in front of the sensor in cm
        return distance
         
        # we're no longer using the GPIO, so tell software we're done
        GPIO.cleanup()
 
    else:
        print("Incorrect usonic() function varible.")
 
try:
    distanceFront = []
    distanceRier = []
    
    i = 0
    while True:
        
        temp = read_adt7410()
        #print ("temperature[C] =", round(temp,1))
        #print ("\tdistance to obstcle = ", round(reading_sonic(0,temp),1), "[cm]")
        #time.sleep(0.01)
        #print(reading_sonic(0, temp))

        
        distData = reading_sonic(0, temp)
        
        distanceFront.append(distData)
        distanceRier.append(distData)
        print(distanceFront)
        print("Front:", distanceFront[i], "Rier:", distanceRier[i])
        
        i = i+1
        
        if i > 10:
            
            with open(saveName,'a') as f:
                writer = csv.writer(f)
                writer.writerow(distanceFront)
                writer.writerow(distanceRier)
            
            break
            
        
except KeyboardInterrupt:
    pass
 
GPIO.cleanup()