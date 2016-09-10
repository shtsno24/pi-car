# -*- coding: utf-8 -*-
import os
import cv2
import time
import picamera
import numpy as np
import picamera.array

cam0 = picamera.PiCamera()
cam0.resolution = (160,128)
cam0.color_effects = (128,128)
path = 'home/pi/test.jpg'
name = 'test.jpg'
if os.path.exists(path) == True:
    os.remove(path)

#capture from camera
stream = picamera.array.PiYUVArray(cam0)
cam0.capture(stream, format = 'yuv', use_video_port = True)

#crop the image and choose Y channel
gray_array = stream.array[0:60, :, 0:1].reshape(1,9600).astype(np.float32)

#save the image
cv2.imwrite(name, gray_array)
