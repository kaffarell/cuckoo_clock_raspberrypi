
#ChangeDutyCycle: 2.5 = 0degree 7.5 = 90degree 12.5 = 180degree

import RPi.GPIO as GPIO
import time

servo_pin = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(servo_pin, GPIO.OUT)

p = GPIO.PWM(servo_pin, 50)
p.start(2.5)
time.sleep(2)
p.ChangeDutyCycle(12.5)
time.sleep(3)
p.ChangeDutyCycle(2.5)
time.sleep(3)
p.stop()
GPIO.cleanup(servo_pin)

