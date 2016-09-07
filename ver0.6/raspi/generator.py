# -*- coding: utf-8 -*-
import os
import gc
import time
import picamera
import numpy as np
import picamera.array
import RPi.GPIO as GPIO

NPZ = 'data.npz'

sl = 0.1
cam0 = picamera.PiCamera()
cam0.resolution = (160, 128)
cam0.color_effects = (128, 128)

left = 5.0
center = 6.2
right = 7.6
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
servo = GPIO.PWM(18,50)

servo.start(0.0)


image_array = np.zeros((1,9600),'float')
label_array = np.zeros((1,4),'float')
k = np.zeros((4, 4), 'float')
for i in range(4):
    k[i, i] = 1
temp_label = np.zeros((1, 4), 'float')


#find NPZ file
if os.path.exists(NPZ) == True:
    with np.load(NPZ) as data:
        print data.files
        train_temp = data['train']
        train_labels_temp = data['train_labels']
    image_array = np.vstack((image_array, train_temp))
    label_array = np.vstack((label_array, train_labels_temp))
    print (train_temp.shape)
    print (train_labels_temp.shape)


while True:
    try:
        while True:
            i1put = raw_input(">")
            
            #capture from camera
            stream = picamera.array.PiRGBArray(cam0)
            cam0.capture(stream, format = 'bgr', use_video_port = True)

            #crop the image
            frame,ret = np.split(stream.array, [60], axis = 0)
            temp_array = frame.reshape(1,9600,3).astype(np.float32)

            #gray scale
            gray_array = temp_array.mean(axis = 2, dtype = int)
            gray_array = gray_array.astype(np.float32)

            del stream, ret, temp_array 
            gc.collect()

            #left
            if i1put == 'a':
                servo.ChangeDutyCycle(left)
                image_array = np.vstack((image_array, gray_array))
                label_array = np.vstack((label_array, k[0]))

            #right
            elif i1put == 'd':
                servo.ChangeDutyCycle(right)
                image_array = np.vstack((image_array, gray_array))
                label_array = np.vstack((label_array, k[2]))

            #forward
            elif i1put == 'w':
                servo.ChangeDutyCycle(center)
                image_array = np.vstack((image_array, gray_array))
                label_array = np.vstack((label_array, k[1]))

            #stop
            elif i1put == 's':
                servo.ChangeDutyCycle(center)
                image_array = np.vstack((image_array, gray_array))
                label_array = np.vstack((label_array, k[3]))
                GPIO.output(24,False)
                GPIO.output(23,False)

            #quit
            elif i1put == 'q':
                break

            else:
                GPIO.output(24,False)
                GPIO.output(23,False)

            time.sleep(1.0)
            GPIO.output(24,False)
            GPIO.output(23,True)
            time.sleep(sl)
            GPIO.output(24,False)
            GPIO.output(23,False)

    except:
        raw_input(">>")

    finally:
        GPIO.output(24,False)
        GPIO.output(23,False)
        servo.stop()
        cam0.close()
        GPIO.cleanup()

        train = image_array[1:, :]
        train_labels = label_array[1:, :]

        np.savez(NPZ, train=train, train_labels=train_labels)
        break

