# -*- coding: utf-8 -*-
print "loading..."

import gc
import os
import sys
import time
import picamera
import numpy as np
import picamera.array
import RPi.GPIO as GPIO
from pybrain.tools.customxml import NetworkReader


XML = 'net.xml' 

cam0 = picamera.PiCamera()
cam0.resolution = (160,128)
cam0.color_effects = (128, 128)
cam0.framerate = 60

sl = 0.05
left = 4.8
center = 6.2
right = 7.8
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
servo = GPIO.PWM(18,50)

servo.start(0.0)

#find XML file
if os.path.exists(XML) == False:
    print('XML file does not exist!')
    raw_input(">")
    sys.exit()

# create network
network = NetworkReader.readFrom(XML)
    
time.sleep(1.0)
print "ready"
time.sleep(1.0)


while True:
    try:
        while True:
                        
            #capture from camera
            stream = picamera.array.PiRGBArray(cam0)
            cam0.capture(stream, format = 'bgr', use_video_port = True)
            
            
            #crop the image
            frame,ret = np.split(stream.array, [60], axis = 0)
            temp_array = frame.reshape(1,9600,3).astype(np.float32)
                        

            t1 = time.time()
            #gray scale
            gray_array = temp_array.mean(axis = 2, dtype = int)
            gray_array = gray_array.astype(np.float32)
            del frame, ret, temp_array
            gc.collect()
            print('%ffps' % (1/(time.time() - t1)))

            #steer
            temp = network.activate(gray_array[0])
            steer = temp.argmax(-1)
            del gray_array
            gc.collect()


            if steer == 0:
                servo.ChangeDutyCycle(left)
            elif steer == 1:
                servo.ChangeDutyCycle(center)
            elif steer == 2:
                servo.ChangeDutyCycle(right)
            elif steer == 3:
                servo.ChangeDutyCycle(center)
                GPIO.output(23,False)
                GPIO.output(24,False)
                print("stop")
                raw_input('>')
            GPIO.output(23,True)
            GPIO.output(24,False)
            time.sleep(sl)
            GPIO.output(23,False)
            GPIO.output(24,False)


    finally:
        gc.collect()
        servo.stop()
        GPIO.cleanup()
        cam0.close()
        break

raw_input('>>')




