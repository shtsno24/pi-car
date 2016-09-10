# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time


left = 5.2
right = 7.8
center = 6.5
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
servo = GPIO.PWM(18,50)

servo.start(0.0)

i = input(">")

while True:
        try:
                while True:
                        GPIO.output(24,True)
                        GPIO.output(23,False)
                	servo.ChangeDutyCycle(left)
                        time.sleep(2.5)
                	GPIO.output(24,False)
                        GPIO.output(23,False)
                        servo.ChangeDutyCycle(center)
                        time.sleep(2.5)
                	GPIO.output(24,False)
                        GPIO.output(23,True)
                	servo.ChangeDutyCycle(right)
                        time.sleep(2.5)
                        GPIO.output(24,False)
                        GPIO.output(23,False)
                	servo.ChangeDutyCycle(center)
                        time.sleep(2.5)
                	i -= 1
                        if i <= 0:
                                break                        
        finally:
                time.sleep(0.5)
                servo.stop()
                GPIO.cleanup()
                break

raw_input('>>')
	
