#!/usr/bin/env python
# -*- coding: utf-8 -*-
# HC-SR04 ultrasonic range sensor
# with ADT7410 temperature sensor for sonic velocity correction
# ultrasonic
#   GPIO 17 output  = "Trig"
#   GPIO 27 input = "Echo"


#sensor1:rightfront
#sensor2:rightrear
#sensor3:left
#sensor4:front

print("dis_4sens.py is being read.")
 
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
saveName = "test092"

sens1_out='SPI2_MOSI'
sens1_in='DAP4_FS'
sens2_out='GPIO_PE6'
sens2_in='GPIO_PZ0'
sens3_out='SPI1_SCK'
sens3_in='SPI1_MISO'
sens4_out='UART2_RTS'
sens4_in='SPI2_SCK'

# prepare for HC-SR04 ultrasonic sensor
GPIO.setwarnings(False)
GPIO.setmode(GPIO.TEGRA_SOC)
#センサ1
GPIO.setup(sens1_out,GPIO.OUT)
GPIO.setup(sens1_in,GPIO.IN)
#センサ2
GPIO.setup(sens2_out,GPIO.OUT)
GPIO.setup(sens2_in,GPIO.IN)
#センサ3
GPIO.setup(sens3_out,GPIO.OUT)
GPIO.setup(sens3_in,GPIO.IN)
#センサ4
#GPIO.setup(sens4_out,GPIO.OUT)
#GPIO.setup(sens4_in,GPIO.IN)

print("よばれてますよ")

# detect temperature in C
def readTemp():
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
 
#sensor

def readSonic(sensor, temp):
    signaloff = 0.0
    distance = 201
    isLoop = (signaloff==0.0) | (distance >200)
    while isLoop:
        if sensor == 1:
            GPIO.output(sens1_out, GPIO.LOW) 
            time.sleep(0.3)
            # send a 10us plus to Trigger
            GPIO.output(sens1_out, True)
            time.sleep(0.00001)        
            GPIO.output(sens1_out, False)
            # detect TTL level signal on Echo
            while GPIO.input(sens1_in) == 0:
                signaloff = time.time()
            while GPIO.input(sens1_in) == 1:
                signalon = time.time()


        elif sensor == 2:
            GPIO.output(sens2_out, GPIO.LOW)
            time.sleep(0.3)
            # send a 10us plus to Trigger
            GPIO.output(sens2_out, True)
            time.sleep(0.00001)        
            GPIO.output(sens2_out, False)
            # detect TTL level signal on Echo
            while GPIO.input(sens2_in) == 0:
                signaloff = time.time()
            while GPIO.input(sens2_in) == 1:
                signalon = time.time()

        elif sensor == 3:
            GPIO.output(sens3_out, GPIO.LOW)
            time.sleep(0.3)
            # send a 10us plus to Trigger
            GPIO.output(sens3_out, True)
            time.sleep(0.00001)        
            GPIO.output(sens3_out, False)
            # detect TTL level signal on Echo
            while GPIO.input(sens3_in) == 0:
                signaloff = time.time()
            while GPIO.input(sens3_in) == 1:
                signalon = time.time()


        elif sensor == 4:
            #センサ4
            GPIO.setup(sens4_out,GPIO.OUT)
            GPIO.setup(sens4_in,GPIO.IN)
            
            GPIO.output(sens4_out, GPIO.LOW) 
            time.sleep(0.3)
            # send a 10us plus to Trigger
            GPIO.output(sens4_out, True)
            time.sleep(0.00001)        
            GPIO.output(sens4_out, False)
            # detect TTL level signal on Echo
            while GPIO.input(sens4_in) == 0:
                signaloff = time.time()
            while GPIO.input(sens4_in) == 1:
                signalon = time.time()
            GPIO.cleanup()

        else:
            print("Incorrect usonic() function varible.")

        # calculate the time interval
        timepassed = signalon - signaloff
         
        # we now have our distance but it's not in a useful unit of
        # measurement. So now we convert this distance into centimetres
        distance = timepassed * (331.50 + 0.606681 * temp) * 100 / 2
        
        # re-calculate isLoop to decide whether go out from while roop

        #print(distance)
        isLoop = (signaloff == 0.0) | (distance >200.0)

    # return the distance of an object in front of the sensor in cm
    return distance
         
    # we're no longer using the GPIO, so tell software we're done
    GPIO.cleanup()
 
    