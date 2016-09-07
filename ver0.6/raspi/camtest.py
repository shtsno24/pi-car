# -*- coding: utf-8 -*-
import os
import cv2
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
stream = picamera.array.PiRGBArray(cam0)
cam0.capture(stream, format = 'bgr', use_video_port = True)

#crop the image
frame,ret = np.split(stream.array, [60], axis = 0)

#gray scale
gray_array = frame.mean(axis = 2, dtype = int)
gray_array = gray_array.astype(np.float32)

#save the image
cv2.imwrite(name, gray_array)
